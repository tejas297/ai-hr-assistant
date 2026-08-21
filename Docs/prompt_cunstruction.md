you can see that in our project we have developed the prompt builder.

it's main job is to combine :
1. system instructions
2. retrieved HR context
3. Employee question

into one structured prompt for LLM.

- This is important because we don't want to simply send the retrieved text to the model. We need to explicitly tell the model:
```
     You are an HR assistant. Answer using only the supplied policy context. If the context doesn't contain the answer, don't invent one.
```