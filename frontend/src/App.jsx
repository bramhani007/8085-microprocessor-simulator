import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "https://eight085-simulator.onrender.com";

function App() {

  const [assemblyCode, setAssemblyCode] = useState(
    `MVI A, 00H
MVI B, 05H
MVI C, 03H

LOOP:
ADD B
DCR C
JNZ LOOP

HLT`
  );

  const [state, setState] = useState(null);
  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState("Ready");

  // =====================================================
  // NUMBER PARSER
  // =====================================================

  const parseNumber = (value) => {

    if (!value) {
      throw new Error("Missing numeric value");
    }

    const input = value
      .trim()
      .toUpperCase();

    let result;

    // HEXADECIMAL
    if (input.endsWith("H")) {

      result = parseInt(
        input.slice(0, -1),
        16
      );
    }

    // BINARY
    else if (input.endsWith("B")) {

      result = parseInt(
        input.slice(0, -1),
        2
      );
    }

    // DECIMAL
    else {

      result = parseInt(
        input,
        10
      );
    }

    if (
      Number.isNaN(result) ||
      result < 0 ||
      result > 0xFFFF
    ) {

      throw new Error(
        `Invalid number: ${value}`
      );
    }

    return result;
  };

  // =====================================================
  // REGISTER OPCODE TABLE
  // =====================================================

  const registerCodes = {

    B: 0b000,
    C: 0b001,
    D: 0b010,
    E: 0b011,
    H: 0b100,
    L: 0b101,
    A: 0b111

  };

  // =====================================================
  // INSTRUCTION SIZE
  // =====================================================

  const getInstructionSize = (line) => {

    const parts = line
      .replace(",", " ")
      .trim()
      .split(/\s+/);

    const instruction = parts[0];

    // 2-BYTE INSTRUCTIONS
    if (instruction === "MVI") {
      return 2;
    }

    // 3-BYTE INSTRUCTIONS
    if (

      instruction === "JMP" ||
      instruction === "JNZ" ||
      instruction === "JC" ||
      instruction === "JNC"

    ) {

      return 3;
    }

    // 1-BYTE INSTRUCTIONS
    return 1;
  };

  // =====================================================
  // GET JUMP ADDRESS
  // =====================================================

  const resolveAddress = (target, labels) => {

    if (!target) {

      throw new Error(
        "Missing jump address or label"
      );
    }

    // LABEL
    if (
      labels[target] !== undefined
    ) {

      return labels[target];
    }

    // NUMERIC ADDRESS
    return parseNumber(target);
  };

  // =====================================================
  // ASSEMBLER
  // =====================================================

  const assembleProgram = (code) => {

    // =================================================
    // CLEAN SOURCE CODE
    // =================================================

    const rawLines = code
      .split("\n")
      .map((line) => {

        // Remove comments
        const withoutComment =
          line.split(";")[0];

        return withoutComment
          .trim()
          .toUpperCase();

      })
      .filter(
        (line) => line !== ""
      );

    // =================================================
    // PASS 1
    // FIND LABEL ADDRESSES
    // =================================================

    const labels = {};

    let address = 0;

    for (let originalLine of rawLines) {

      let line = originalLine;

      // ---------------------------------------------
      // LABEL ONLY
      // ---------------------------------------------

      if (
        line.endsWith(":")
      ) {

        const label =
          line
            .slice(0, -1)
            .trim();

        if (
          !label
        ) {

          throw new Error(
            `Invalid label: ${originalLine}`
          );
        }

        if (
          labels[label] !== undefined
        ) {

          throw new Error(
            `Duplicate label: ${label}`
          );
        }

        labels[label] = address;

        continue;
      }

      // ---------------------------------------------
      // LABEL + INSTRUCTION
      // ---------------------------------------------

      if (
        line.includes(":")
      ) {

        const separatorIndex =
          line.indexOf(":");

        const label =
          line
            .slice(0, separatorIndex)
            .trim();

        line =
          line
            .slice(separatorIndex + 1)
            .trim();

        if (
          labels[label] !== undefined
        ) {

          throw new Error(
            `Duplicate label: ${label}`
          );
        }

        labels[label] = address;
      }

      // ---------------------------------------------
      // CALCULATE INSTRUCTION SIZE
      // ---------------------------------------------

      address +=
        getInstructionSize(line);
    }

    // =================================================
    // PASS 2
    // GENERATE MACHINE CODE
    // =================================================

    const machineCode = [];

    for (
      let originalLine of rawLines
    ) {

      let line = originalLine;

      // ---------------------------------------------
      // LABEL ONLY
      // ---------------------------------------------

      if (
        line.endsWith(":")
      ) {

        continue;
      }

      // ---------------------------------------------
      // REMOVE LABEL
      // ---------------------------------------------

      if (
        line.includes(":")
      ) {

        const separatorIndex =
          line.indexOf(":");

        line =
          line
            .slice(separatorIndex + 1)
            .trim();
      }

      // ---------------------------------------------
      // TOKENIZE
      // ---------------------------------------------

      const parts = line
        .replace(",", " ")
        .trim()
        .split(/\s+/);

      const instruction =
        parts[0];

      const operand1 =
        parts[1];

      const operand2 =
        parts[2];

      // =================================================
      // NOP
      // =================================================

      if (
        instruction === "NOP"
      ) {

        machineCode.push(
          0x00
        );
      }

      // =================================================
      // MVI
      // =================================================

      else if (
        instruction === "MVI"
      ) {

        const register =
          operand1;

        const value =
          parseNumber(
            operand2
          );

        const mviOpcodes = {

          A: 0x3E,
          B: 0x06,
          C: 0x0E,
          D: 0x16,
          E: 0x1E,
          H: 0x26,
          L: 0x2E

        };

        if (
          mviOpcodes[register]
          === undefined
        ) {

          throw new Error(
            `Invalid MVI register: ${register}`
          );
        }

        if (
          value > 0xFF
        ) {

          throw new Error(
            `MVI value must be 8-bit: ${operand2}`
          );
        }

        machineCode.push(

          mviOpcodes[register],
          value

        );
      }

      // =================================================
      // MOV
      // =================================================

      else if (
        instruction === "MOV"
      ) {

        const destination =
          operand1;

        const source =
          operand2;

        if (

          registerCodes[destination]
          === undefined ||

          registerCodes[source]
          === undefined

        ) {

          throw new Error(
            `Invalid MOV instruction: ${line}`
          );
        }

        const opcode =

          0x40 |

          (
            registerCodes[destination]
            << 3
          ) |

          registerCodes[source];

        // 0x76 is HLT
        if (
          opcode === 0x76
        ) {

          throw new Error(
            "MOV M, M is not valid"
          );
        }

        machineCode.push(
          opcode
        );
      }

      // =================================================
      // ADD
      // =================================================

      else if (
        instruction === "ADD"
      ) {

        const addOpcodes = {

          B: 0x80,
          C: 0x81,
          D: 0x82,
          E: 0x83,
          H: 0x84,
          L: 0x85,
          A: 0x87

        };

        if (
          addOpcodes[operand1]
          === undefined
        ) {

          throw new Error(
            `Invalid ADD instruction: ${line}`
          );
        }

        machineCode.push(
          addOpcodes[operand1]
        );
      }

      // =================================================
      // SUB
      // =================================================

      else if (
        instruction === "SUB"
      ) {

        const subOpcodes = {

          B: 0x90,
          C: 0x91,
          D: 0x92,
          E: 0x93,
          H: 0x94,
          L: 0x95,
          A: 0x97

        };

        if (
          subOpcodes[operand1]
          === undefined
        ) {

          throw new Error(
            `Invalid SUB instruction: ${line}`
          );
        }

        machineCode.push(
          subOpcodes[operand1]
        );
      }

      // =================================================
      // INR
      // =================================================

      else if (
        instruction === "INR"
      ) {

        const inrOpcodes = {

          A: 0x3C,
          B: 0x04,
          C: 0x0C,
          D: 0x14,
          E: 0x1C,
          H: 0x24,
          L: 0x2C

        };

        if (
          inrOpcodes[operand1]
          === undefined
        ) {

          throw new Error(
            `Invalid INR instruction: ${line}`
          );
        }

        machineCode.push(
          inrOpcodes[operand1]
        );
      }

      // =================================================
      // DCR
      // =================================================

      else if (
        instruction === "DCR"
      ) {

        const dcrOpcodes = {

          A: 0x3D,
          B: 0x05,
          C: 0x0D,
          D: 0x15,
          E: 0x1D,
          H: 0x25,
          L: 0x2D

        };

        if (
          dcrOpcodes[operand1]
          === undefined
        ) {

          throw new Error(
            `Invalid DCR instruction: ${line}`
          );
        }

        machineCode.push(
          dcrOpcodes[operand1]
        );
      }

      // =================================================
      // MUL B
      // =================================================

      else if (

        instruction === "MUL" &&
        operand1 === "B"

      ) {

        machineCode.push(
          0xE8
        );
      }

      // =================================================
      // DIV B
      // =================================================

      else if (

        instruction === "DIV" &&
        operand1 === "B"

      ) {

        machineCode.push(
          0xE9
        );
      }

      // =================================================
      // JMP
      // =================================================

      else if (
        instruction === "JMP"
      ) {

        const target =
          resolveAddress(
            operand1,
            labels
          );

        machineCode.push(

          0xC3,

          target & 0xFF,

          (target >> 8) & 0xFF

        );
      }

      // =================================================
      // JNZ
      // =================================================

      else if (
        instruction === "JNZ"
      ) {

        const target =
          resolveAddress(
            operand1,
            labels
          );

        machineCode.push(

          0xC2,

          target & 0xFF,

          (target >> 8) & 0xFF

        );
      }

      // =================================================
      // JC
      // =================================================

      else if (
        instruction === "JC"
      ) {

        const target =
          resolveAddress(
            operand1,
            labels
          );

        machineCode.push(

          0xDA,

          target & 0xFF,

          (target >> 8) & 0xFF

        );
      }

      // =================================================
      // JNC
      // =================================================

      else if (
        instruction === "JNC"
      ) {

        const target =
          resolveAddress(
            operand1,
            labels
          );

        machineCode.push(

          0xD2,

          target & 0xFF,

          (target >> 8) & 0xFF

        );
      }

      // =================================================
      // HLT
      // =================================================

      else if (
        instruction === "HLT"
      ) {

        machineCode.push(
          0x76
        );
      }

      // =================================================
      // UNKNOWN INSTRUCTION
      // =================================================

      else {

        throw new Error(
          `Unsupported instruction: ${line}`
        );
      }
    }

    return machineCode;
  };

  // =====================================================
  // LOAD PROGRAM
  // =====================================================

  const loadProgram = async () => {

    try {

      const machineCode =
        assembleProgram(
          assemblyCode
        );

      console.log(
        "Generated Machine Code:",
        machineCode
      );

      const response =
        await axios.post(

          `${API_URL}/load`,

          {
            program: machineCode
          }

        );

      setState(
        response.data.state
      );

      setHistory(
        []
      );

      setMessage(

        `Program loaded successfully | ` +

        machineCode

          .map((byte) =>

            byte

              .toString(16)

              .toUpperCase()

              .padStart(2, "0")

          )

          .join(" ")

      );

    }

    catch (error) {

      console.error(
        error
      );

      setMessage(

        error.response?.data?.detail ||

        error.message ||

        "Error loading program"

      );
    }
  };

  // =====================================================
  // STEP PROGRAM
  // =====================================================

  const stepProgram = async () => {

    try {

      const response =
        await axios.post(

          `${API_URL}/step`

        );

      setState(
        response.data.state
      );

      if (
        response.data.result
      ) {

        setHistory(

          (previous) => [

            ...previous,

            response.data.result

          ]

        );
      }

      setMessage(
        "One instruction executed"
      );
    }

    catch (error) {

      console.error(
        error
      );

      setMessage(

        error.response?.data?.detail ||

        error.message ||

        "Error executing instruction"

      );
    }
  };

  // =====================================================
  // RUN PROGRAM
  // =====================================================

  const runProgram = async () => {

    try {

      const response =
        await axios.post(

          `${API_URL}/run`,

          {
            max_steps: 1000
          }

        );

      setState(
        response.data.state
      );

      setHistory(
        response.data.history || []
      );

      setMessage(
        "Program execution completed"
      );
    }

    catch (error) {

      console.error(
        error
      );

      setMessage(

        error.response?.data?.detail ||

        error.message ||

        "Error running program"

      );
    }
  };

  // =====================================================
  // RESET CPU
  // =====================================================

  const resetProgram = async () => {

    try {

      const response =
        await axios.post(

          `${API_URL}/reset`

        );

      setState(
        response.data.state
      );

      setHistory(
        []
      );

      setMessage(
        "CPU reset successfully"
      );
    }

    catch (error) {

      console.error(
        error
      );

      setMessage(
        "Error resetting CPU"
      );
    }
  };

  // =====================================================
  // FORMAT REGISTER VALUE
  // =====================================================

  const getRegisterValue = (register) => {

    return (

      state?.registers?.[register] ??
      "00"

    );
  };

  // =====================================================
  // FORMAT SPECIAL REGISTER
  // =====================================================

  const getSpecialRegisterValue = (
    register,
    defaultValue
  ) => {

    return (

      state?.registers?.[register] ??
      defaultValue

    );
  };

  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="app">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div>

          <h1>
            8085 Microprocessor Simulator
          </h1>

          <p>
            Assembly Language Debugger & Visual Simulator
          </p>

        </div>

        <div className="status">

          <span className="status-dot"></span>

          Backend Connected

        </div>

      </header>

      {/* =================================================
          DASHBOARD
      ================================================= */}

      <main className="dashboard">

        {/* =================================================
            ASSEMBLY EDITOR
        ================================================= */}

        <section className="editor-panel card">

          <h2>
            Assembly Editor
          </h2>

          <textarea

            value={
              assemblyCode
            }

            onChange={

              (event) =>

                setAssemblyCode(
                  event.target.value
                )

            }

            placeholder=
            "Write 8085 assembly code here..."

          />

          {/* MACHINE CODE PREVIEW */}

          <div className="machine-code-preview">

            <strong>
              Generated Machine Code:
            </strong>

            <code>

              {(() => {

                try {

                  return assembleProgram(
                    assemblyCode
                  )

                    .map((byte) =>

                      byte

                        .toString(16)

                        .toUpperCase()

                        .padStart(2, "0")

                    )

                    .join(" ");

                }

                catch (error) {

                  return "Invalid instruction";

                }

              })()}

            </code>

          </div>

          {/* CONTROLS */}

          <div className="controls">

            <button
              onClick={
                loadProgram
              }
            >
              LOAD
            </button>

            <button

              onClick={
                stepProgram
              }

              disabled={
                !state ||
                state.halted
              }

            >
              STEP
            </button>

            <button

              onClick={
                runProgram
              }

              disabled={
                !state ||
                state.halted
              }

            >
              RUN
            </button>

            <button
              onClick={
                resetProgram
              }
            >
              RESET
            </button>

          </div>

          <div className="message">

            {message}

          </div>

        </section>

        {/* =================================================
            CPU REGISTERS
        ================================================= */}

        <section className="card">

          <h2>
            CPU Registers
          </h2>

          <div className="register-grid">

            {[
              "A",
              "B",
              "C",
              "D",
              "E",
              "H",
              "L"

            ].map(

              (register) => (

                <div

                  className="register"

                  key={
                    register
                  }

                >

                  <span>
                    {register}
                  </span>

                  <strong>

                    {
                      getRegisterValue(
                        register
                      )
                    }

                  </strong>

                </div>

              )

            )}

          </div>

          <div className="special-registers">

            <div>

              <span>
                PC
              </span>

              <strong>

                {
                  getSpecialRegisterValue(
                    "PC",
                    "0000"
                  )
                }

              </strong>

            </div>

            <div>

              <span>
                SP
              </span>

              <strong>

                {
                  getSpecialRegisterValue(
                    "SP",
                    "FFFF"
                  )
                }

              </strong>

            </div>

            <div>

              <span>
                IR
              </span>

              <strong>

                {
                  getSpecialRegisterValue(
                    "IR",
                    "00"
                  )
                }

              </strong>

            </div>

          </div>

        </section>

        {/* =================================================
            FLAGS
        ================================================= */}

        <section className="card">

          <h2>
            Flags
          </h2>

          <div className="flags-grid">

            {[
              "S",
              "Z",
              "AC",
              "P",
              "CY"

            ].map(

              (flag) => (

                <div

                  className={

                    `flag ${state?.flags?.[flag] === 1
                      ? "active"
                      : ""
                    }`

                  }

                  key={
                    flag
                  }

                >

                  <span>
                    {flag}
                  </span>

                  <strong>

                    {
                      state?.flags?.[flag] ??
                      0
                    }

                  </strong>

                </div>

              )

            )}

          </div>

        </section>

        {/* =================================================
            EXECUTION TRACE
        ================================================= */}

        <section className="card">

          <h2>
            Execution Trace
          </h2>

          <div className="trace">

            {

              history.length === 0

                ? (

                  <p className="empty">

                    No instructions executed yet

                  </p>

                )

                : (

                  history.map(

                    (item, index) => (

                      <div

                        className="trace-row"

                        key={
                          index
                        }

                      >

                        <span>

                          Step {
                            index + 1
                          }

                        </span>

                        <strong>

                          {
                            item.opcode
                          }

                        </strong>

                        <span>

                          {
                            item.instruction
                          }

                        </span>

                      </div>

                    )

                  )

                )

            }

          </div>

        </section>

        {/* =================================================
            SYSTEM INFORMATION
        ================================================= */}

        <section className="card system-info">

          <h2>
            System Information
          </h2>

          <div className="info-grid">

            <div>

              <span>
                Cycles
              </span>

              <strong>

                {
                  state?.cycles ??
                  0
                }

              </strong>

            </div>

            <div>

              <span>
                CPU Status
              </span>

              <strong>

                {

                  state?.halted

                    ? "HALTED"

                    : "READY"

                }

              </strong>

            </div>

            <div>

              <span>
                Architecture
              </span>

              <strong>
                8085
              </strong>

            </div>

            <div>

              <span>
                Data Width
              </span>

              <strong>
                8-bit
              </strong>

            </div>

          </div>

        </section>

      </main>

    </div>

  );
}

export default App;