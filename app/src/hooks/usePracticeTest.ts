import { useCallback, useEffect, useState } from "react";
import testData from "../data/practice-test-1.json";
import type { AppState, Mistake, PracticeTest, QuestionResult } from "../types";

const STORAGE_KEY = "econ351-practice-test-1";

const defaultState: AppState = {
  currentIndex: 0,
  results: {},
  mistakes: [],
  started: false,
  showAnswer: {},
};

function loadState(): AppState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultState;
    return { ...defaultState, ...JSON.parse(raw) };
  } catch {
    return defaultState;
  }
}

export function usePracticeTest() {
  const data = testData as PracticeTest;
  const [state, setState] = useState<AppState>(loadState);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const current = data.questions[state.currentIndex];

  const recordMistake = useCallback(
    (userAnswer: string, correctAnswer: string) => {
      const q = data.questions[state.currentIndex];
      const mistake: Mistake = {
        questionNum: q.num,
        bankId: q.bankId,
        label: q.label,
        category: q.category,
        chapter: q.chapter,
        userAnswer,
        correctAnswer,
        timestamp: new Date().toISOString(),
      };
      setState((s) => ({
        ...s,
        mistakes: [
          mistake,
          ...s.mistakes.filter((m) => m.questionNum !== q.num),
        ],
      }));
    },
    [data.questions, state.currentIndex]
  );

  const markResult = useCallback(
    (correct: boolean, userAnswer: string) => {
      const q = data.questions[state.currentIndex];
      const result: QuestionResult = { num: q.num, correct, answered: true };
      setState((s) => ({
        ...s,
        results: { ...s.results, [q.num]: result },
        showAnswer: { ...s.showAnswer, [q.num]: true },
      }));
      if (!correct) {
        recordMistake(userAnswer, q.correctOption || q.answerKey);
      }
    },
    [data.questions, state.currentIndex, recordMistake]
  );

  const submitMc = useCallback(
    (selected: string) => {
      const q = data.questions[state.currentIndex];
      const correct =
        selected === q.correctOption ||
        (q.correct && selected.trim().startsWith(`(${q.correct})`));
      markResult(!!correct, selected);
    },
    [data.questions, state.currentIndex, markResult]
  );

  const submitSelf = useCallback(
    (gotIt: boolean) => {
      markResult(gotIt, gotIt ? "Self: correct" : "Self: incorrect");
    },
    [markResult]
  );

  const goTo = (index: number) => {
    setState((s) => ({
      ...s,
      currentIndex: Math.max(0, Math.min(index, data.questions.length - 1)),
    }));
  };

  const startTest = () => setState((s) => ({ ...s, started: true }));

  const resetAll = () => {
    localStorage.removeItem(STORAGE_KEY);
    setState(defaultState);
  };

  const toggleAnswer = () => {
    const q = data.questions[state.currentIndex];
    setState((s) => ({
      ...s,
      showAnswer: { ...s.showAnswer, [q.num]: !s.showAnswer[q.num] },
    }));
  };

  const answered = Object.values(state.results).filter((r) => r.answered).length;
  const correctCount = Object.values(state.results).filter((r) => r.correct).length;
  const wrongCount = Object.values(state.results).filter(
    (r) => r.answered && !r.correct
  ).length;

  return {
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
  };
}
