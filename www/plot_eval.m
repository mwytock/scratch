
A = [18 2 0
     11 7 2 
     20 0 0
     19 1 0];
bar([A; mean(A)])
colormap([0     0.322 0.796; 
          0.694 0.188 0.6;
          1     0.149 0.227]);
legend('APUSH', 'Same', 'Google', 'Orientation', 'horizontal', 'Location', 'NorthOutside');

set(gca, 'XTickLabel', { 'Teacher 1', 'Teacher 2', 'Teacher 3', 'Teacher 4', ...
                    'Average'}, ...
         'FontSize', 6);
ylabel('Number of times preferred');



prepare_figure('teacher_eval.pdf', [3.32 2]);
         


    
                    
