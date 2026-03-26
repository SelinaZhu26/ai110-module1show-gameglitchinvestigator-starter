# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  When I first opened the game, I noticed a few things. The settings were on the left with 3 diffulty levels. Furthermore, the attempts allowed under settings didn't match with the game attempts number. Most importantly of all, the hints were the opposite of what they actually were. Furthermore, the "New Game" button doesn't even work.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  First off, the difficulty settings of Easy, Medium, and Hard were wrong because they should be in ascending order of number guessing range but they weren't. The biggest error of the game was that the instructions were completely wrong because it would tell you to go higher when it your guess was actually lower and vice versa. Another mistake I noticed was that the 'New Game' button didn't work and I had to manually refresh the page to get a new game. 


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I only used Copilot and Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

I asked AI to state some bugs they see in the code with the context of the website being a higher or lower numbers game. One that was stated was the hints being wrong. This was indeed a valid bug. AI said "If the guess is too high, the hint says "Go HIGHER" — the opposite of what it should say. The messages are swapped." After this, I manually went in the code and swapped the hints so that they were right myself.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

There was surprisingly no instance of this for me so Not Applicable (N/A)

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I corrected the bug in the code and then checked the game to see if it was actually fixed in the way I hoped it would be.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  One test I ran was with the difficulty ranges. After I fixed them, I ran the game and they were accurately showing the diffuclty ranges this time.

- Did AI help you design or understand any tests? How?

  The testing part was personally confusing for me. I would ask the chatbot to create the tests but then it would keep asking me to make the edit or not and after 5 times of clicking yes, I wasn't sure where it had gone. But never the less, the error was fixed in the actual game so that was the test I needed.



---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

On even-numbered attempts, the secret was converted to a string (e.g., "42"), but your guess stayed an integer (42). When check_guess compared them, an integer can never equal a string in Python, so it would always say "Too High" or "Too Low" — even if you guessed the right number.

On odd-numbered attempts, the secret was kept as an integer, so comparison worked normally.The actual secret number stored in session_state.secret never changed — but the type the game compared against alternated between int and string each attempt, making it behave like a moving target. You could guess the right number and still be told you were wrong, just because you guessed on an even attempt.


- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit rerases and redraws the entire script from top to bottom every time the user does anything, like clicking a button or typing — this is called a "rerun." This means normal Python variables reset on every rerun, so something like secret = random.randint(1, 100) would generate a new number on every click, making the game unwinnable. st.session_state is like a sticky notepad that survives reruns — values stored there persist as long as the browser tab is open. By wrapping the secret in an if "secret" not in st.session_state check, the number is only generated once and then saved to that notepad for all future reruns. In short, session state is the only way to keep information alive across Streamlit's constant reruns.

- What change did you make that finally gave the game a stable secret number?

Looking at the code, the secret number was already stable — it's stored in st.session_state.secret with the guard check on line 96–97. That pattern was already correct in the starter code. The actual bug wasn't that the secret changed — it was that on even-numbered attempts, the secret was cast to a string before comparison (lines 162–163), making correct guesses appear wrong.

So if you fixed the game, the key change would have been removing the int/string alternating logic and always comparing against the raw integer.


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

One habit worth carrying forward: read the code before trusting the symptoms.

In this project, the bug looked like the secret number was changing, but reading the code revealed the real cause was a type mismatch. If you had just guessed at fixes based on the surface behavior, you might have added unnecessary resets or re-randomization logic and never solved the actual problem. Getting in the habit of tracing exactly what the code does — line by line — before jumping to a fix will save a lot of time in future projects.


  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?

One thing to do differently: test each AI-suggested change in isolation before accepting it.

In this project, the AI introduced multiple bugs at once — the type mismatch, the flipped hints, the broken difficulty ranges. If you had tested after each individual change rather than letting fixes pile up, you would have caught which specific suggestion introduced which bug, instead of having to untangle several problems at once.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI-generated code can look completely reasonable on the surface while hiding subtle, hard-to-spot bugs — so it needs the same skeptical review you'd give any untrusted code. This project made clear that AI is a fast first draft, not a finished answer.