//returns number of paths P: from 'scr' to 'destinatn' having length 'len'
//n is the number of nodes
//graph is the adjacency matrix of the graph
long long int paths(bool graph[][200], int n, int src, int destinatn, int len, bool traversed[])
{
    //if len == 1 the only possible path is a direct edge
    if (len == 1 and graph[src][destinatn]) return 1;
    if (len == 1 and !graph[src][destinatn]) return 0;

    //to avoid infinite loops
    //otherwise nodes called by 'src', will again call 'src' following an infinte loop
    traversed[src] = true;
    long long int ans = 0;

    //traversing all neighbors of 'src'
    for (int j = 0; j < n; ++j) if (!traversed[j] and graph[src][j])
    {
        ans += paths(graph, n, j, destinatn, len - 1, traversed);
    }

    //to allow particaipation of 'src' in other cycles also
    traversed[src] = false;
    
    return ans;
}
