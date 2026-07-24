from fastapi import APIRouter, HTTPException

from .schemas import (
    LoadProgramRequest,
    RunProgramRequest
)

from ..core.cpu8085 import CPU8085


router = APIRouter(

    prefix="/api/simulator",

    tags=["8085 Simulator"]

)


# =====================================================
# GLOBAL CPU INSTANCE
# =====================================================

cpu = CPU8085()


# =====================================================
# CPU STATE HELPER
# =====================================================

def get_cpu_state():

    return {

        "registers": cpu.registers.get_state(),

        "flags": cpu.flags.get_state(),

        "pc": cpu.registers.PC,

        "sp": cpu.registers.SP,

        "ir": cpu.registers.IR,

        "halted": cpu.halted,

        "cycles": cpu.cycles,

        "psw": cpu.get_psw()

    }


# =====================================================
# HEALTH CHECK
# =====================================================

@router.get("/health")
def health_check():

    return {

        "status": "ok",

        "message": "8085 Simulator Backend is running"

    }


# =====================================================
# LOAD PROGRAM
# =====================================================

@router.post("/load")
def load_program(request: LoadProgramRequest):

    try:

        # Reset CPU before loading

        cpu.reset()

        # Validate every byte

        for byte in request.program:

            if not 0 <= byte <= 0xFF:

                raise ValueError(

                    f"Invalid byte: {byte}"

                )

        # Load program into memory

        for address, byte in enumerate(

            request.program

        ):

            cpu.memory.write(

                address,

                byte

            )

        return {

            "status": "loaded",

            "program_size": len(

                request.program

            ),

            "state": get_cpu_state()

        }

    except Exception as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)

        )


# =====================================================
# GET CPU STATE
# =====================================================

@router.get("/state")
def get_state():

    return get_cpu_state()


# =====================================================
# EXECUTE ONE INSTRUCTION
# =====================================================

@router.post("/step")
def step_cpu():

    try:

        result = cpu.step()

        return {

            "status": "success",

            "result": result,

            "state": get_cpu_state()

        }

    except Exception as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)

        )


# =====================================================
# RUN PROGRAM
# =====================================================

@router.post("/run")
def run_program(

    request: RunProgramRequest

):

    try:

        steps = 0

        history = []

        while (

            not cpu.halted

            and steps < request.max_steps

        ):

            result = cpu.step()

            history.append(result)

            steps += 1

        return {

            "status": (

                "halted"

                if cpu.halted

                else "max_steps_reached"

            ),

            "steps": steps,

            "history": history,

            "state": get_cpu_state()

        }

    except Exception as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)

        )


# =====================================================
# RESET CPU
# =====================================================

@router.post("/reset")
def reset_cpu():

    cpu.reset()

    return {

        "status": "reset",

        "state": get_cpu_state()

    }