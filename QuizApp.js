const express = require("express");
const bodyParser = require("body-parser");
const QuizApp = express();
const path = require("path");
QuizApp.use(bodyParser.urlencoded({ extended: true }));
QuizApp.use((req, res, next) => {
    res.setHeader("Content-Type", "text/html; charset = UTF-8");
    next();
});
QuizApp.set("view engine", "ejs");
QuizApp.set("view cache", false);
QuizApp.use(express.static(path.join(__dirname, "public")));
const questions = [
    { question: "1. For which team(s) did Giovanni Ferrari score the most goals in Serie A?", choices: ['Lecco', 'Bari', 'Pro Patria', 'Juventus', 'Pescara'], correct: "Juventus" },
    { question: "2. When did Gianni Rivera debut in Serie A?", choices: ['1962', '1956', '1955', '1959', '1958'], correct: "1958" },
    { question: "3. How many Serie A goals did Roberto Bettega score?", choices: ['125', '101', '129', '137', '100'], correct: "129" },
    { question: "4. How many matches did Alessandro Altobelli play for Juventus in Serie A?", choices: ['33', '43', '20', '30', '29'], correct: "20" },
    { question: "5. How many goals per game did Marek Hamšík average in Serie A?", choices: ['0.22', '0.37', '0.33', '0.24', '0.38'], correct: "0.24" },
    { question: "6. When did Alessandro Del Piero debut in Serie A?", choices: ['1993', '1990', '1989', '1991', '1994'], correct: "1993" },
    { question: "7. Which Serie A team(s) has Pietro Anastasi played for?", choices: ['Lucchese, Varese, Lecco, Ascoli and Parma', 'Varese, Juventus, Internazionale and Ascoli', 'Lucchese', 'Internazionale and Ascoli', 'Parma'], correct: "Varese, Juventus, Internazionale and Ascoli" },
    { question: "8. How many matches did Omar Sívori play for Napoli in Serie A?", choices: ['114', '63', '69', '122', '120'], correct: "63" },
    { question: "9. For which team(s) did Gunnar Nordahl score the most goals in Serie A?", choices: ['Juventus', 'Milan and Juventus', 'Pescara', 'Torino', 'Milan'], correct: "Milan" },
    { question: "10. Which Serie A team(s) has Sergio Pellissier played for?", choices: ['Roma and Chievo', 'Chievo', 'Milan', 'Milan, Roma and Chievo', 'Milan and Roma'], correct: "Chievo" },
    { question: "11. Which Serie A team(s) has Ezio Pascutti played for?", choices: ['Varese', 'Bologna, Messina and Varese', 'Varese and Messina', 'Bologna', 'Messina and Bologna'], correct: "Bologna" },
    { question: "12. How many matches did Cristiano Lucarelli play for Lecce in Serie A?", choices: ['43', '45', '59', '75', '62'], correct: "59" },
    { question: "13. For which team(s) did Giovanni Ferrari score the most goals in Serie A?", choices: ['Parma and Foggia', 'Chievo', 'Juventus', 'Foggia', 'Parma'], correct: "Juventus" },
    { question: "14. For which team(s) did Gabriel Batistuta score the most goals in Serie A?", choices: ['Chievo', 'Ancona', 'Bologna', 'Fiorentina', 'Lucchese'], correct: "Fiorentina" },
    { question: "15. Which Serie A team(s) has Aldo Boffi played for?", choices: ['Lecce', 'Milan and Lecce', 'Milan', 'Lecce, Cagliari and Milan', 'Lecce and Cagliari'], correct: "Milan" },
    { question: "16. How many Serie A goals did Abel Balbo score?", choices: ['94', '91', '96', '117', '90'], correct: "117" },
    { question: "17. How many Serie A goals did Sergio Clerici score?", choices: ['109', '98', '105', '99', '103'], correct: "103" },
    { question: "18. When did Alessandro Altobelli debut in Serie A?", choices: ['1974', '1978', '1980', '1977', '1976'], correct: "1977" },
    { question: "19. How many goals per game did John Hansen average in Serie A?", choices: ['0.56', '0.65', '0.58', '0.57', '0.55'], correct: "0.65" },
    { question: "20. How many Serie A goals did Giuseppe Savoldi score?", choices: ['168', '184', '176', '182', '174'], correct: "168" }
];
QuizApp.get("/", (req, res) => res.render("index"));
QuizApp.get("/quiz", (req, res) => res.render("quiz", { questions: questions }));
QuizApp.post("/result", (req, res) => {
    const answers = req.body;
    let score = 0;
    for (let i = 0; i < questions.length; i++) if (answers[`q${i}`] === questions[i].correct) score++;
    res.render("result", { score: score, total: questions.length });
});
QuizApp.listen(3000, () => { console.log("QuizApp server is listening on port 3000");});