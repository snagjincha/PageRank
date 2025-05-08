import gzip

# 최대 노드 번호를 계산
def max_nodes(file_path):
    max_node = -1
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue # 주석 생략
            origin, dest = map(int, line.split())
            max_node = max(max_node, origin, dest)
    return max_node + 1

file_path = 'web-Google.txt.gz'
max_node = max_nodes(file_path)

# row_coor는 출발지, col_coor는 도착지
def CRS_matrix(file_path, num_nodes):
    col_coor = []     # 열 인덱스
    row_coor = [0]    # 행 인덱스
    out_degree = [0] * max_node

    with gzip.open(file_path, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue # 주석 생략
            origin, dest = map(int,line.split()) # 데이터를 출발지와 도착지로 구분
            col_coor.append(dest) # 도착지점을 y축처럼 열에 저장
            out_degree[origin] += 1 # out degree를 계산

    # 출발 지점을 x축처럼 행에 저장(출발지가 중복되는 경우를 대비하여 누적합으로 저장)
    cumulative_count = 0
    for count in out_degree:
        cumulative_count += count # 각 행이 어디서 시작하는 지를 누적합을 통해 아는 것.
        row_coor.append(cumulative_count)

    return row_coor, col_coor, out_degree

file_path = 'web-Google.txt.gz'
num_nodes = max_node
row_coor, col_coor, out_degree = CRS_matrix(file_path, num_nodes)

# power iteration
def power_iteration(col_coor, row_coor, out_degree ,n, beta=0.85, T=100, epsilon=1e-6):
    r = [1 / n] * n  # 초기 값 설정

    for t in range(T):
        r_new = [0] * n  # 새로운 r 값
        r_prime = [0] * n
        S = 0

        # r' = β * A^T * r^(t)
        for i in range(n):
            if out_degree[i] > 0:  # out-degree가 0이 아닌 경우만 계산 (다른 노드로 pagerank 값을 전파할 수 없다.)
                for j in range(row_coor[i], row_coor[i + 1]):  # i번 노드의 연결된 모든 도착 노드 탐색 ex) row_coor[0]=4라면 0번 노드에서 뻗어나간 연결의 수가 4개라는 것.
                    r_prime[col_coor[j]] += beta * r[i] / out_degree[i] # 출발노드(row_coor)에서 도착노드(col_coor)으로 뻗어나간 여러 개의 노드를 누적합한 것이 r_prime
                    # ex) row_coor[0]=4라면 0번 노드에서의 out-degree가 4라는 의미고 도착노드 4개가 col_coor[0]... col_coor[3]을 돌면서 누적합을 계산. 그것을 r_prime으로 저장. 

        # r'의 합으로 S(sum of non-leaked scores)를 구함.
        S = sum(r_prime)

        # r_new = r' + (1 - S)/ n
        for i in range(n):
            r_new[i] += r_prime[i] + (1 - S) / n

        diff = sum(abs(r_new[i] - r[i]) for i in range(n))
        if diff < epsilon:
            break

        r = r_new

    return r

Pagerank_score = power_iteration(col_coor, row_coor, out_degree, max_node)

result = sorted(enumerate(Pagerank_score), key=lambda x: x[1], reverse=True)
print(result[:10])