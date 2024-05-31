# SerieAQuiz
A Node.js quiz about Serie A goalscoring records with programmatic questions. Requires Python and Node.js.

The questions are built based upon a table scraped from: https://en.wikipedia.org/wiki/List_of_Serie_A_players_with_100_or_more_goals. Run `main.py` to generate the questions.

Afterwards, set up a new Node.js project in the same folder:

```npm init -y```

Install dependencies:

```
npm install express
npm install body-parser
npm install path
```

Run the quiz with:

```node QuizApp.js```

Open it by typing ```http://localhost:3000/``` into a browser address bar.

![image](https://github.com/andrei-stoica26/SerieAQuiz/assets/44497020/a2dd6fee-5f37-4897-9b21-805bef066443)

