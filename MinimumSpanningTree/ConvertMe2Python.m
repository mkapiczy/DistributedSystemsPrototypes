clear;
clc;
M = [0 8 0 3;
    8 0 2 5;
    0 2 0 6;
    3 5 6 0];
% Get amount of nodes
N = length(M);
% Calculate amount of edges
Nmax = N-1;
% Replace zeros or should be ignored values with below calculated
Vmax = max(max(M))+1000;
M(M==0) = Vmax;
% Initialize index and vectors
Midx = (zeros(N,N));
v1 = zeros(N,3);
% Note - Row: [Edge Weight, From Node, To Node]
v_finale = nan(Nmax,3);
% For each node...
for i1 = 1:N
    % Maximize values we do not wish to evaluate.
    % We use the inverse index matrix to ensure mirrowed already taken
    % values are removed
    M(logical(Midx')) = Vmax;
    % Find min and save value and column index

    [v1(i1,1),v1(i1,3)] = min(M(i1,:));
    % Save row index
    v1(i1,2) = i1;
    % Ensure we mark the edge as noted
    Midx(i1,v1(i1,3)) = 1;
end
% For each edge...
for i2 = 1:Nmax
    % Find the minimum of all the current edges
    [~,idx_temp]= min(v1(:,1));
    % Save it to finale list of edges 
    v_finale(i2,:) = [v1(idx_temp,1) v1(idx_temp,2) v1(idx_temp,3)];
    % Remove the chosen edge
    v1(idx_temp,:) = [];
end
% Initialize K to remake a index matrix
K = zeros(N,N);
% For each node selected
for i3 = 1:Nmax
    % Insert the edge weight within the connected nodes (row/columns)
    K(v_finale(i3,2),v_finale(i3,3)) = v_finale(i3,1);
end