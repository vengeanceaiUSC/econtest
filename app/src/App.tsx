import { usePracticeTest } from "./hooks/usePracticeTest";
import "./App.css";

function App() {
  const {
    data,
    state,
    current,
    answered,
    correctCount,
    wrongCount,
    startTest,
    resetAll,
    goTo,
    submitMc,
    submitSelf,
    toggleAnswer,
  } = usePracticeTest();

  const result = state.results[current.num];
  const showAnswer = state.showAnswer[current.num];
  const isComplete = answered === data.totalQuestions;

  if (!state.started) {
    return (
      <div className="app">
        <header className="hero">
          <p className="eyebrow">ECON 351 · Midterm Simulation</p>
          <h1>{data.title}</h1>
          <p className="subtitle">
            24 questions · Ch. 4 (12) + Ch. 9 (12) · Clickable practice test
          </p>
          <div className="format-grid">
            <div className="format-card">
              <h3>Part A — Ch. 4</h3>
              <ul>
                <li>2 consumer</li>
                <li>2 labor-leisure</li>
                <li>2 intertemporal</li>
                <li>3 elasticity</li>
                <li>1 budget line</li>
                <li>2 preferences</li>
              </ul>
            </div>
            <div className="format-card">
              <h3>Part B — Ch. 9</h3>
              <ul>
                <li>5 insurance</li>
                <li>4 risk attitudes</li>
                <li>2 CE &amp; RP</li>
                <li>1 diversification</li>
              </ul>
            </div>
          </div>
          {state.mistakes.length > 0 && (
            <p className="resume-note">
              {state.mistakes.length} mistake(s) saved from last session
            </p>
          )}
          <button className="btn primary" onClick={startTest}>
            {answered > 0 ? "Resume Practice Test" : "Start Practice Test"}
          </button>
        </header>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <strong>{data.title}</strong>
          <span className="muted">
            Q{current.num} of {data.totalQuestions}
          </span>
        </div>
        <div className="stats">
          <span className="stat ok">{correctCount} right</span>
          <span className="stat bad">{wrongCount} wrong</span>
          <span className="stat">{answered}/{data.totalQuestions} done</span>
        </div>
      </header>

      <nav className="qnav">
        {data.questions.map((q, i) => {
          const r = state.results[q.num];
          let cls = "qdot";
          if (i === state.currentIndex) cls += " active";
          if (r?.answered) cls += r.correct ? " correct" : " wrong";
          return (
            <button key={q.num} className={cls} onClick={() => goTo(i)}>
              {q.num}
            </button>
          );
        })}
      </nav>

      <main className="main">
        <section className="question-card">
          <div className="meta">
            <span className="chip">Ch. {current.chapter}</span>
            <span className="chip">{current.category}</span>
            <span className="chip muted">{current.label}</span>
          </div>
          <p className="source">{current.source}</p>
          <h2 className="prompt">{current.question}</h2>

          {current.mode === "mc" && !result?.answered && (
            <div className="options">
              {current.options.map((opt) => (
                <button
                  key={opt}
                  className="option"
                  onClick={() => submitMc(opt)}
                >
                  {opt}
                </button>
              ))}
            </div>
          )}

          {current.mode === "self" && !result?.answered && (
            <div className="self-grade">
              <p className="hint">
                Work the problem on paper, then check yourself.
              </p>
              <div className="self-btns">
                <button
                  className="btn ok"
                  onClick={() => submitSelf(true)}
                >
                  I got it right
                </button>
                <button
                  className="btn bad"
                  onClick={() => submitSelf(false)}
                >
                  I got it wrong
                </button>
              </div>
              <button className="btn ghost" onClick={toggleAnswer}>
                {showAnswer ? "Hide answer" : "Show answer key"}
              </button>
              {showAnswer && (
                <div className="answer-box">
                  <strong>Answer key</strong>
                  <p>{current.answerKey}</p>
                  {current.notes && <p className="notes">{current.notes}</p>}
                </div>
              )}
            </div>
          )}

          {result?.answered && (
            <div className={`feedback ${result.correct ? "ok" : "bad"}`}>
              <strong>
                {result.correct ? "Correct!" : "Recorded as wrong"}
              </strong>
              {!result.correct && (
                <p>
                  Added to your mistake log. Review the answer key below.
                </p>
              )}
              <div className="answer-box">
                <strong>Answer key</strong>
                <p>{current.answerKey}</p>
                {current.notes && <p className="notes">{current.notes}</p>}
              </div>
            </div>
          )}

          <div className="nav-btns">
            <button
              className="btn ghost"
              disabled={state.currentIndex === 0}
              onClick={() => goTo(state.currentIndex - 1)}
            >
              ← Previous
            </button>
            <button
              className="btn primary"
              disabled={state.currentIndex === data.questions.length - 1}
              onClick={() => goTo(state.currentIndex + 1)}
            >
              Next →
            </button>
          </div>
        </section>

        <aside className="sidebar">
          <h3>Mistake Log</h3>
          {state.mistakes.length === 0 ? (
            <p className="muted">No mistakes recorded yet.</p>
          ) : (
            <ul className="mistake-list">
              {state.mistakes.map((m) => (
                <li key={m.questionNum}>
                  <button
                    className="mistake-item"
                    onClick={() =>
                      goTo(data.questions.findIndex((q) => q.num === m.questionNum))
                    }
                  >
                    <span className="mistake-q">Q{m.questionNum}</span>
                    <span className="mistake-cat">{m.category}</span>
                    <span className="mistake-you">You: {m.userAnswer}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}

          {isComplete && (
            <div className="summary">
              <h4>Test Complete</h4>
              <p>{correctCount} / {data.totalQuestions} correct</p>
              <p>{wrongCount} mistakes logged</p>
            </div>
          )}

          <button className="btn ghost danger" onClick={resetAll}>
            Reset all progress
          </button>
        </aside>
      </main>
    </div>
  );
}

export default App;
