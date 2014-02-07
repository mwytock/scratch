% Simple visualization for the optimization algorithm in R^2

f = @(x) exp((x(1)+2)+3*(x(2)-0.2)-0.1) + exp((x(1)+2)-3*(x(2)-0.2)-0.1) + exp(-(x(1)+1.5)-0.1);
dim = [4 2.67];

[X Y] = meshgrid(sort([linspace(-5,0.8,1000) 0]), sort([linspace(-2,2,1000) 0]));
Z = exp((X+2)+3.*(Y-0.2)-0.1) + exp((X+2)-3.*(Y-0.2)-0.1) + exp(-(X+1.5)-0.1);

b = [.204 .596 .859];
r = [.906 .298 .235];

figure;
contour(X, Y, log(Z), linspace(1.5, 3, 5), 'Color', [0.6 0.6 0.6]);
hold on;
plot([-5 1], [0 0], 'Color', 'w');
plot([0 0], [-1.9 2.1], 'Color', 'w');

set(gca, 'Position', [0 0 1 1], ...
         'Visible', 'off');
set(gcf, 'InvertHardCopy', 'off', 'Color', 'k')
prepare_figure('vis1.pdf', dim);

% starting point
x = zeros(6,2);
x(1,:) = [-4 1];

for iter=1:5
    % values for l1 norm
    Z1 = 4*abs(Y);

    % values for second order approximation
    [g H] = numdiff(f, x(iter,:)');
    dX = X - x(iter,1);
    dY = Y - x(iter,2);
    fx = f(x(iter,:));
    Z2 = fx + g(1)*dX+g(2)*dY + ...
         0.5*dX.*H(1,1).*dX + dX.*H(1,2).*dY + 0.5*dY.*H(2,2).*dY;

    [min_x i] = min(Z1(:) + Z2(:));
    x(iter+1,1) = X(i);
    x(iter+1,2) = Y(i);

    if iter == 1
        text(x(1,1), x(1,2), ' x^{(0)}', ...
             'VerticalAlignment', 'top', ...
             'HorizontalAlignment', 'left', ...
             'Color', 'w');
        plot(x(1,1), x(1,2), 'wo', 'MarkerFaceColor', 'w');
        prepare_figure('vis2.pdf', dim);

        contour(X, Y, Z2, fx, 'Color', b, 'LineWidth', 1);
        prepare_figure('vis3.pdf', dim);

        % Show where the next point would be with no regularization
        [min_x i] = min(Z2(:));
        tmp(1) = plot(X(i), Y(i), 'wo', 'MarkerFaceColor', 'w', ...
                      'MarkerEdgeColor', 'w');
        tmp(2) = text(X(i), Y(i), ' x^{(1)''}', ...
                      'VerticalAlignment', 'top', ...
                      'HorizontalAlignment', 'left', ...
                      'Color', 'w');
        prepare_figure('vis3a.pdf', dim);

        % Draw the l1 contour at the next point
        Z3 = abs(X) + abs(Y);
        contour(X, Y, Z3, abs(x(iter+1,1)), 'Color', b, 'LineWidth', 1);
        prepare_figure('vis3b.pdf', dim);

        delete(tmp);
    elseif iter == 2
        text(x(2,1), x(2,2), 'x^{(1)} ', ...
             'VerticalAlignment', 'top', ...
             'HorizontalAlignment', 'right', ...
             'Color', 'w');
        plot(x(2,1), x(2,2), 'wo', 'MarkerFaceColor', 'w', ...
             'MarkerEdgeColor', 'w');
        prepare_figure('vis4.pdf', dim);

        contour(X, Y, Z2, fx, 'Color', r, 'LineWidth', 1);
        prepare_figure('vis5.pdf', dim);
    elseif iter == 3
        plot(x(3,1), x(3,2), 'wo', 'MarkerFaceColor', 'w', ...
             'MarkerEdgeColor', 'w');
        prepare_figure('vis6.pdf', dim);
    elseif iter == 4
        plot(x(4,1), x(4,2), 'wo', 'MarkerFaceColor', 'w', ...
             'MarkerEdgeColor', 'w');
        prepare_figure('vis7.pdf', dim);
    end

    x'
end
