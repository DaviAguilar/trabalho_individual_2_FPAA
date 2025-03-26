import matplotlib.pyplot as plt
import networkx as nx
import os

def maxmin_select(arr, low, high, G=None, parent=None, level=0):
    if G is None:
        G = nx.DiGraph()

    node_id = f"{low}-{high}"
    node_label = f"[{', '.join(map(str, arr[low:high + 1]))}]\\nLevel {level}"
    G.add_node(node_id, label=node_label)

    if parent:
        G.add_edge(parent, node_id)

    print(f"Nível de recursão {level}: processando {arr[low:high + 1]}")

    if low == high:
        G.nodes[node_id]['label'] = f"[{arr[low]}]\\nMax={arr[low]}, Min={arr[low]}\\nLevel {level}"
        print(f"Base case: um elemento {arr[low]}")
        return arr[low], arr[low], G

    if high == low + 1:
        if arr[low] > arr[high]:
            max_val, min_val = arr[low], arr[high]
        else:
            max_val, min_val = arr[high], arr[low]
        G.nodes[node_id]['label'] = f"[{arr[low]}, {arr[high]}]\\nMax={max_val}, Min={min_val}\\n1 comp\\nLevel {level}"
        print(f"Base case: dois elementos {arr[low]} e {arr[high]}, max={max_val}, min={min_val}")
        return max_val, min_val, G

    mid = (low + high) // 2
    max1, min1, G = maxmin_select(arr, low, mid, G, node_id, level + 1)
    max2, min2, G = maxmin_select(arr, mid + 1, high, G, node_id, level + 1)

    final_max = max(max1, max2)
    final_min = min(min1, min2)
    G.nodes[node_id]['label'] = f"[{', '.join(map(str, arr[low:high + 1]))}]\\nMax={final_max}, Min={final_min}\\n2 comp\\nLevel {level}"

    print(f"Nível de recursão {level}: combinado {arr[low:high + 1]}, max={final_max}, min={final_min}")

    return final_max, final_min, G

def find_max_min(arr):
    if not arr:
        return None, None, None
    max_val, min_val, G = maxmin_select(arr, 0, len(arr) - 1)

    pos = nx.spring_layout(G, k=50)  # Ajusta o espaçamento dos nós
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=2500, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray')
    plt.savefig('diagrama_maxmin.png')
    plt.close()

    return max_val, min_val

if __name__ == "__main__":
    arr = [258, 2, 67, 52, 1, 102, 305,48]
    maximum, minimum = find_max_min(arr)
    print(f"Array: {arr}")
    print(f"Max: {maximum}, Min: {minimum}")
    print("Diagrama gerado em '/diagrama_maxmin.png'")
