"use client";

export function FeedbackButtons({
  onFeedback,
  onReplace,
}: {
  onFeedback: (event: string) => void;
  onReplace: (direction: string) => void;
}) {
  return (
    <p>
      <button onClick={() => onFeedback("like")}>♥ 喜欢</button>
      <button onClick={() => onFeedback("dislike")}>× 不喜欢</button>
      <button onClick={() => onFeedback("skip")}>跳过</button>
      <button onClick={() => onReplace("similar")}>→ 相似</button>
      <button onClick={() => onReplace("explore")}>→ 探索</button>
      <button onClick={() => onReplace("different")}>→ 不同</button>
    </p>
  );
}
