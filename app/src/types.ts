export interface ExamSection {
  ch: number;
  category: string;
  count: number;
}

export interface Question {
  num: number;
  bankId: string;
  label: string;
  chapter: number;
  category: string;
  source: string;
  question: string;
  mode: "mc" | "self";
  options: string[];
  correct: string | null;
  correctOption: string | null;
  answerKey: string;
  notes: string;
  type: string;
}

export interface PracticeTest {
  title: string;
  totalQuestions: number;
  structure: ExamSection[];
  questions: Question[];
}

export interface Mistake {
  questionNum: number;
  bankId: string;
  label: string;
  category: string;
  chapter: number;
  userAnswer: string;
  correctAnswer: string;
  timestamp: string;
}

export interface QuestionResult {
  num: number;
  correct: boolean;
  answered: boolean;
}

export interface AppState {
  currentIndex: number;
  results: Record<number, QuestionResult>;
  mistakes: Mistake[];
  started: boolean;
  showAnswer: Record<number, boolean>;
}
