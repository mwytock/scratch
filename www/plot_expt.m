
% Precision 
P = [0.82 0.825 0.82 0.807 0.78
     0.72 0.68 0.657 0.67 0.66];

% Recall
R = repmat(100:100:500, [], 2) .* P / 989;


figure;
plot(R', P', 'LineWidth', 1);
hold on;
box off;
plot(0:0.1:0.4, ones(5,1)*0.56, 'k--', 'LineWidth', 1)
legend('Similarity', 'Knowledge base', 'Random');
set(gca, 'FontSize', 8)
axis([0 0.4 0.5 1])
prepare_figure('expt.pdf', [3.32 2.5], 'Recall', 'Precision');

P = [0.9  0.88 0.833 0.815 0.784
     0.88 0.83 0.837 0.813 0.768
     0.82 0.825 0.82 0.807 0.78
     0.79 0.74 0.7   0.68  0.67
     0.72 0.68 0.657 0.67  0.66
    ];

% Recall
R = repmat(100:100:500, [], 5) .* P / 989;

figure;
hold on;
plot(R(1,:), P(1,:), 'r', 'LineWidth', 1);
plot(R(2,:), P(2,:), 'b', 'LineWidth', 1);
plot(R(3,:), P(3,:), 'b--', 'LineWidth', 1);
plot(R(4,:), P(4,:), 'Color', [0 0.5 0], 'LineWidth', 1);
plot(R(5,:), P(5,:), '--', 'Color', [0 0.5 0], 'LineWidth', 1);
legend('Hybrid', 'Sim + Relevance', 'Similarity', 'KB + Relevance', ...
       'Knowledge base');
prepare_figure('expt2.pdf', [3.32 2.5], 'Recall', 'Precision');
set(gca, 'FontSize', 8);
axis([0 0.5 0.65 1])
prepare_figure('expt_relevance.pdf', [3.32 2.5], 'Recall', 'Precision');

