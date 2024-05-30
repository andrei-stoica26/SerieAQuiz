import pandas as pd

def write_js():
    with open('QuizApp.js', 'w', encoding = 'utf-8') as f:
        df = pd.read_csv('Output/quiz.csv')
        n_questions = df.shape[0]
        questions = [f'{i}. {x}' for i, x in enumerate(df['Question'], 1)]
        choices = df[['A', 'B', 'C', 'D', 'E']].values.tolist()
        correct = [df.iloc[i][df.iloc[i]['Correct']] for i in range(n_questions)]
        questions_join = ',\n    '.join([f'{{ question: "{questions[i]}", choices: {choices[i]}, correct: "{correct[i]}" }}' for i in range(n_questions)])
        questions_str = f'\nconst questions = [\n    {questions_join}\n];\n'
        f.write('\n'.join(['const express = require("express");',
                       'const bodyParser = require("body-parser");',
                       'const QuizApp = express();',
                       'const path = require("path");',
                       'QuizApp.use(bodyParser.urlencoded({ extended: true }));',
                       'QuizApp.use((req, res, next) => {',
                       '    res.setHeader("Content-Type", "text/html; charset = UTF-8");',
                       '    next();',
                       '});',
                       'QuizApp.set("view engine", "ejs");',
                       'QuizApp.set("view cache", false);',
                       'QuizApp.use(express.static(path.join(__dirname, "public")));'
                       ]))
        f.write(questions_str)
        f.write('\n'.join(['QuizApp.get("/", (req, res) => res.render("index"));',
                      'QuizApp.get("/quiz", (req, res) => res.render("quiz", { questions: questions }));',
                       'QuizApp.post("/result", (req, res) => {',
                       '    const answers = req.body;',
                       '    let score = 0;',
                       '    for (let i = 0; i < questions.length; i++) if (answers[`q${i}`] === questions[i].correct) score++;',
                       '    res.render("result", { score: score, total: questions.length });',
                       '});',
                       'QuizApp.listen(3000, () => { console.log("QuizApp server is listening on port 3000");});']))
        
def main():
    write_js()

if __name__ == '__main__':
    main()
    


    
