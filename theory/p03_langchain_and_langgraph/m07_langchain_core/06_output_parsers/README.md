# M07.6 Theory: Output parsers

*[M07 theory](../README.md) · Lesson 7.6 · Notebooks: [`06a_Output_Parser.ipynb`](../../../../course/p03_langchain_and_langgraph/m07_langchain_core/notebooks/06a_Output_Parser.ipynb) · [All theory pages](../../../README.md)*

## Output parsers

An output parser is the last step of a chain, `prompt | llm | parser`. It works in two places: before the call, `get_format_instructions()` returns text that goes into the prompt; after it, `parse()` turns the reply text into a Python value or raises `OutputParserException`.

| Parser | Returns | Raises when |
|---|---|---|
| `StrOutputParser` | the reply text | never |
| `CommaSeparatedListOutputParser` | a list of strings | never; `"Sure: a, b"` becomes `['Sure: a', 'b']` |
| `JsonOutputParser` | whatever JSON it finds, usually a dict | it finds no JSON it can repair |
| `PydanticOutputParser` | an instance of your model | no JSON, or the JSON fails the model's validation |

`JsonOutputParser` is more forgiving than its name suggests. In `langchain-core` 1.7.0 it strips whitespace and backticks, looks inside a ```` ```json ```` fence, and when the JSON is incomplete it closes open strings and brackets and drops trailing characters until something parses. `PydanticOutputParser` runs that same JSON step, then validates the result against the schema. A parser only checks what the schema states, and a reply can be valid JSON and still wrong.

The [interactive lab](interactive/parser-bench-lab.html) runs eight representative replies to the Larkspur refund question through four parsers. The replies are hand-written, since no model was called; the parsers are JavaScript ports of the library code, which agree with `langchain-core` 1.7.0 and Pydantic 2.14.1 on all 4,452 checks (1,113 reply texts, including every truncation of the eight replies, times four parsers). Its counts:

| Parser | Raised | Returned, unusable | Usable |
|---|---|---|---|
| `StrOutputParser` | 0 | 8 | 0 |
| `JsonOutputParser` | 1 | 4 | 3 |
| `PydanticOutputParser`, `list[str]` ids | 3 | 2 | 3 |
| `PydanticOutputParser`, `Literal` ids | 5 | 0 | 3 |

"Usable" is the lab's own rule: an answer string and at least one citation that names one of the three passages. The table shows four things:

- **The usable count never moves.** Three replies are good (clean, fenced, and one with a trailing note, which the repair step drops) and every parser that reads fields accepts them. A stricter parser does not produce more good answers; it moves bad ones from the returned column to the raised column, where a retry or a fallback can catch them.
- **`JsonOutputParser` raises on one reply only**: the one with prose before unfenced JSON. It returns the truncated reply, the reply with no `citations` key, the one with citations as a string and the one with an invented id, each as an ordinary dict.
- **`list[str]` stops the shape errors but not the made-up ids.** The missing key and the string raise; `"refund-win"` (a truncated id) and `"handbook-p4"` (an invented one) are strings, so they pass.
- **A `Literal` of the passage ids raises on all five.** The schema now states the rule the lab grades by.

<!-- lab: interactive/parser-bench-lab.html -->

Truncation is where the repair step matters most. Cutting the clean 124-character reply at each of its 125 lengths, as a `max_tokens` limit would: `JsonOutputParser` raises on 1 cut (the empty one) and returns a dict for the other 124, of which 4 are usable. `PydanticOutputParser` with `list[str]` raises on 107 and returns 14 unusable answers, such as a citation cut to `"refund-t"`. With `Literal` ids it raises on 120; the one unusable cut it lets through is `"citations": []`, cut just after the bracket, which no `Literal` can catch. A `min_length=1` on the list would catch it, at the cost of refusing an honest "the handbook does not say" with no citations.

The schema behind the `Literal` row:

```python
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

PassageId = Literal["refund-window", "refund-timing", "billing"]

class CitedAnswer(BaseModel):
    answer: str = Field(description="The answer, using only the passages")
    citations: list[PassageId] = Field(description="Ids of the passages the answer uses")

parser = PydanticOutputParser(pydantic_object=CitedAnswer)
chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
```

The three ids are fixed here because the lab has one question. In a live pipeline the retrieved ids change per question, so either build the `Literal` per request or check the ids against the retrieved set right after parsing. The check has to exist somewhere; the lab shows what happens where it does not.

## Check that the instructions arrive

Format instructions only help if they reach the model. The prompt needs a `{format_instructions}` slot, filled with `.partial()` or `partial_variables`, as notebook 06a does. The instructions are long: for the two-field schema, the lab measures 748 characters from `PydanticOutputParser` and 1,301 from `JsonOutputParser(pydantic_object=...)`, sent as input tokens on every call.

The optional notebook [`07f_output_parsers_demo.ipynb`](../../../../course/p03_langchain_and_langgraph/m07_langchain_core/optional/07f_output_parsers_demo.ipynb) shows the silent version of this mistake. Its `PydanticOutputParser` example calls `.partial(format_instructions=...)` on a template with no `{format_instructions}` slot. LangChain ignores the value without an error, so the model never sees the schema, and the chain works only when the model happens to produce matching JSON from the one-line request. Printing the formatted prompt once shows whether the schema is in it.

---
*Previous: [7.5 Prompt templates and few-shot composition](../05_prompt_templates_and_few_shot_composition/README.md). Next: [7.7 LangChain 1.x recap course, ending in a structured-output Q&A bot](../07_langchain_1_x_recap_course_ending_in_a_structured_output_q_a_bot/README.md).*
