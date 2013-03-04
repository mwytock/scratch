function [p r] = pr(x)
p = x ./ [1:length(x)]';
r = x / x(end);
