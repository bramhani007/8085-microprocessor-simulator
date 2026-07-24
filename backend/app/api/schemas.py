from pydantic import BaseModel, Field


class LoadProgramRequest(BaseModel):

    program: list[int] = Field(

        ...,

        description="8085 machine code bytes"

    )


class RunProgramRequest(BaseModel):

    max_steps: int = Field(

        default=10000,

        ge=1,

        le=100000

    )