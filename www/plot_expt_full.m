
[p0 r0] = pr(load('knowledge.txt'));
[p1 r1] = pr(load('similarity.txt'));
[p2 r2] = pr(load('knowledge_rel.txt'));
[p3 r3] = pr(load('similarity_rel.txt'));
[p4 r4] = pr(load('hybrid.txt'));

figure;
hold on;
plot(r1, p1, 'b', 'LineWidth', 1);
plot(r0, p0, 'Color', [0 0.5 0], 'LineWidth', 1);
plot(0:0.1:1, ones(11,1)*0.56, 'k--', 'LineWidth', 1)
legend('Similarity', 'Knowledge base', 'Random')
set(gca, 'FontSize', 8);
prepare_figure('expt.pdf', [3.45 2.5], 'Recall', 'Precision');

figure;
hold on;
plot(r4, p4, 'r', 'LineWidth', 1);
plot(r3, p3, 'b', 'LineWidth', 1);
plot(r1, p1, 'b--', 'LineWidth', 1);
plot(r2, p2, 'Color', [0 0.5 0], 'LineWidth', 1);
plot(r0, p0, '--', 'Color', [0 0.5 0], 'LineWidth', 1);
set(gca, 'FontSize', 8);
legend('Hybrid', 'Sim + relevance', 'Similarity', 'KB + relevance', ...
       'Knowledge base');
prepare_figure('expt_relevance.pdf', [3.45 2.5], 'Recall', 'Precision');
