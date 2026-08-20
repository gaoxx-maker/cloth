# 推荐

`RuleRecommendationEngine` 调用 scorer 计算兴趣、新奇、质量和随机分数，再由 diversity 重排。探索度提升 novelty/random 权重。替换算法的下一步工作是将当前商品和候选集传给 engine，实现 similar/explore/different 的过滤策略。
