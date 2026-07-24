import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/simulator";

function App() {
  const [assemblyCode, setAssemblyCode] = useState(
    `MVI A, 05H
MVI B, 03H
ADD B
HLT`
  );

  const [state, setState] = useState(null);
  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState("Ready");

  // =====================================================
  // ASSEMBLY CODE → MACHINE CODE
  // =====================================================

  const assembleProgram = (code) => {
    const lines = code
      .split("\n")
      .map((line) => line.trim().toUpperCase())
      .filter((line) => line !== "");

    const machineCode = [];

    for (const line of lines) {
      const parts = line.replace(",", "").split(/\s+/);

      const instruction = parts[0];

      // =========================
      // MVI A, DATA
      // =========================

      if (instruction === "MVI" && parts[1] === "A") {
        const value = parseNumber(parts[2]);

        machineCode.push(0x3E);
        machineCode.push(value);
      }

      // =========================
      // MVI B, DATA
      // =========================

      else if (instruction === "MVI" && parts[1] === "B") {
        const value = parseNumber(parts[2]);

        machineCode.push(0x06);
        machineCode.push(value);
      }

      // =========================
      // MVI C, DATA
      // =========================

      else if (instruction === "MVI" && parts[1] === "C") {
        const value = parseNumber(parts[2]);

        machineCode.push(0x0E);
        machineCode.push(value);
      }

      // =========================
      // MVI D, DATA
      // =========================

      else if (instruction === "MVI" && parts[1] === "D") {
        const value = parseNumber(parts[2]);

        machineCode.push(0x16);
        machineCode.push(value);
      }

      // =========================
      // MVI E, DATA
      // =========================

      else if (instruction === "MVI" && parts[1] === "E") {
        const value = parseNumber(parts[2]);

        machineCode.push(0x1E);
        machineCode.push(value);
      }

      // =========================
      // MVI H, DATA
      // =========================

      else if (instruction === "MVI" && parts[1] === "H") {
        const value = parseNumber(parts[2]);

        machineCode.push(0x26);
        machineCode.push(value);
      }

      // =========================
      // MVI L, DATA
      // =========================

      else if (instruction === "MVI" && parts[1] === "L") {
        const value = parseNumber(parts[2]);

        machineCode.push(0x2E);
        machineCode.push(value);
      }

      // =========================
      // ADD B
      // =========================

      else if (instruction === "ADD" && parts[1] === "B") {
        machineCode.push(0x80);
      }

      // =========================
      // ADD C
      // =========================

      else if (instruction === "ADD" && parts[1] === "C") {
        machineCode.push(0x81);
      }

      // =========================
      // HLT
      // =========================

      else if (instruction === "HLT") {
        machineCode.push(0x76);
      }

      // =========================
      // UNKNOWN INSTRUCTION
      // =========================

      else {
        throw new Error(`Unsupported instruction: ${line}`);
      }
    }

    return machineCode;
  };

  // =====================================================
  // NUMBER PARSER
  // =====================================================

  const parseNumber = (value) => {
    if (!value) {
      throw new Error("Missing numeric value");
    }

    value = value.toUpperCase();

    // Hexadecimal: 05H
    if (value.endsWith("H")) {
      return parseInt(value.slice(0, -1), 16);
    }

    // Binary: 00000101B
    if (value.endsWith("B")) {
      return parseInt(value.slice(0, -1), 2);
    }

    // Decimal: 5
    return parseInt(value, 10);
  };

  // =====================================================
  // LOAD PROGRAM
  // =====================================================

  const loadProgram = async () => {
    try {
      const machineCode = assembleProgram(assemblyCode);

      console.log("Generated Machine Code:", machineCode);

      const response = await axios.post(`${API_URL}/load`, {
        program: machineCode,
      });

      setState(response.data.state);
      setHistory([]);

      setMessage(
        `Program loaded successfully | ${machineCode
          .map((byte) => byte.toString(16).toUpperCase().padStart(2, "0"))
          .join(" ")}`
      );
    } catch (error) {
      console.error(error);

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
      const response = await axios.post(`${API_URL}/step`);

      setState(response.data.state);

      if (response.data.result) {
        setHistory((previous) => [
          ...previous,
          response.data.result,
        ]);
      }

      setMessage("One instruction executed");
    } catch (error) {
      console.error(error);

      setMessage(
        error.response?.data?.detail ||
        "Error executing instruction"
      );
    }
  };

  // =====================================================
  // RUN PROGRAM
  // =====================================================

  const runProgram = async () => {
    try {
      const response = await axios.post(`${API_URL}/run`, {
        max_steps: 100,
      });

      setState(response.data.state);
      setHistory(response.data.history || []);

      setMessage("Program execution completed");
    } catch (error) {
      console.error(error);

      setMessage(
        error.response?.data?.detail ||
        "Error running program"
      );
    }
  };

  // =====================================================
  // RESET CPU
  // =====================================================

  const resetProgram = async () => {
    try {
      const response = await axios.post(`${API_URL}/reset`);

      setState(response.data.state);
      setHistory([]);

      setMessage("CPU reset successfully");
    } catch (error) {
      console.error(error);

      setMessage("Error resetting CPU");
    }
  };

  return (
    <div className="app">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="header">

        <div>
          <h1>8085 Microprocessor Simulator</h1>

          <p>
            Assembly Language Debugger & Visual Simulator
          </p>
        </div>

        <div className="status">

          <span className="status-dot"></span>

          Backend Connected

        </div>

      </header>

      {/* =====================================================
          MAIN DASHBOARD
      ===================================================== */}

      <main className="dashboard">

        {/* =====================================================
            ASSEMBLY EDITOR
        ===================================================== */}

        <section className="editor-panel card">

          <h2>Assembly Editor</h2>

          <textarea
            value={assemblyCode}
            onChange={(event) =>
              setAssemblyCode(event.target.value)
            }
            placeholder="Write 8085 assembly code here..."
          />

          {/* MACHINE CODE PREVIEW */}

          <div className="machine-code-preview">

            <strong>Generated Machine Code:</strong>

            <code>
              {(() => {
                try {
                  return assembleProgram(assemblyCode)
                    .map((byte) =>
                      byte
                        .toString(16)
                        .toUpperCase()
                        .padStart(2, "0")
                    )
                    .join(" ");
                } catch {
                  return "Invalid instruction";
                }
              })()}
            </code>

          </div>

          {/* BUTTONS */}

          <div className="controls">

            <button onClick={loadProgram}>
              LOAD
            </button>

            <button
              onClick={stepProgram}
              disabled={!state || state.halted}
            >
              STEP
            </button>

            <button
              onClick={runProgram}
              disabled={!state || state.halted}
            >
              RUN
            </button>

            <button onClick={resetProgram}>
              RESET
            </button>

          </div>

          <div className="message">

            {message}

          </div>

        </section>

        {/* =====================================================
            CPU REGISTERS
        ===================================================== */}

        <section className="card">

          <h2>CPU Registers</h2>

          <div className="register-grid">

            {[
              "A",
              "B",
              "C",
              "D",
              "E",
              "H",
              "L",
            ].map((register) => (

              <div
                className="register"
                key={register}
              >

                <span>{register}</span>

                <strong>
                  {state?.registers?.[register] || "00"}
                </strong>

              </div>

            ))}

          </div>

          <div className="special-registers">

            <div>

              <span>PC</span>

              <strong>
                {state?.registers?.PC || "0000"}
              </strong>

            </div>

            <div>

              <span>SP</span>

              <strong>
                {state?.registers?.SP || "FFFF"}
              </strong>

            </div>

            <div>

              <span>IR</span>

              <strong>
                {state?.registers?.IR || "00"}
              </strong>

            </div>

          </div>

        </section>

        {/* =====================================================
            FLAGS
        ===================================================== */}

        <section className="card">

          <h2>Flags</h2>

          <div className="flags-grid">

            {[
              "S",
              "Z",
              "AC",
              "P",
              "CY",
            ].map((flag) => (

              <div
                className={`flag ${state?.flags?.[flag] === 1
                  ? "active"
                  : ""
                  }`}
                key={flag}
              >

                <span>{flag}</span>

                <strong>
                  {state?.flags?.[flag] ?? 0}
                </strong>

              </div>

            ))}

          </div>

        </section>

        {/* =====================================================
            EXECUTION TRACE
        ===================================================== */}

        <section className="card">

          <h2>Execution Trace</h2>

          <div className="trace">

            {history.length === 0 ? (

              <p className="empty">
                No instructions executed yet
              </p>

            ) : (

              history.map((item, index) => (

                <div
                  className="trace-row"
                  key={index}
                >

                  <span>
                    Step {index + 1}
                  </span>

                  <strong>
                    {item.opcode}
                  </strong>

                  <span>
                    {item.instruction}
                  </span>

                </div>

              ))

            )}

          </div>

        </section>

        {/* =====================================================
            SYSTEM INFORMATION
        ===================================================== */}

        <section className="card system-info">

          <h2>System Information</h2>

          <div className="info-grid">

            <div>

              <span>Cycles</span>

              <strong>
                {state?.cycles ?? 0}
              </strong>

            </div>

            <div>

              <span>CPU Status</span>

              <strong>
                {state?.halted
                  ? "HALTED"
                  : "READY"}
              </strong>

            </div>

            <div>

              <span>Architecture</span>

              <strong>
                8085
              </strong>

            </div>

            <div>

              <span>Data Width</span>

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