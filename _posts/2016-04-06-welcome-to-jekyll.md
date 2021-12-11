---

 layout: post

 title: "Post Title"

 subtitle: "This is the post subtitle."

 date: YYYY-MM-DD HH:MM:SS

---
 
 Link: https://arxiv.org/pdf/1902.03545.pdf

Основная часть:

Для сравнения задач предлагается использовать векторное представление задач.
Рассмотрим

$$
\Delta KL(p_{w'}(y|x) || p_{w}(y|x)) = \delta w F \delta w + o(||\delta w||^2),
$$
где $F$ - матрица Фишера:

$$
F=\mathbb{E}_{x, y \sim \hat{p}(x) p_{w}(y \mid x)}\left[\nabla_{w} \log p_{w}(y \mid x) \nabla_{w} \log p_{w}(y \mid x)^{T}\right]
$$
градиент тут берется по весам encoder и получается матрица num_params encoder $\times$ num_params encoder.

В качестве векторного представления авторы и предлагают использовать матрицу Фишера. 

В качестве encoder использовался ImageNet pretrained ResNet.
Для упрощения подсчета предлагается использовать: 
- Только диагонали элементы матрицы Фишера (тогда мы не учитываем корреляцию между весами)
- Для весов с одного фильтра сделать значения одинаковыми

Так как авторы считают, что матрица Фишера неустойчива, предлагается считать её не напрямую, а при помощи вариационной аппроксимации

$$
L(\hat{w} ; \Lambda)=\mathbb{E}_{w \sim \mathcal{N}(\hat{w}, \Lambda)} \left[H_{p_{w}, \hat{p}} p(y \mid x)\right] 
+\beta K L\left(\mathcal{N}(0, \Lambda) \| \mathcal{N}\left(0, \lambda^{2} I\right)\right)
$$
Тут мы оптимизируем матрицу $\Lambda$. Решение будет иметь следующий вид:
$$
\frac{\beta}{2 N} \Lambda=F+\frac{\beta \lambda^{2}}{2 N} I
$$
Второй член можно откинуть при большом числе данных.

$$
F=\mathbb{E}_{x, y \sim \hat{p}(x) p_{w}(y \mid x)}\left[(y-p)^{2} \cdot S \otimes x x^{T}\right]
$$
where $p=p_{w}(y=1 \mid x)$ and the matrix $S=w w^{T} \odot z z^{T} \odot$ $(1-z)(1-z)^{T}$ is an element-wise product of classifier.

Из вида  матрицы  Фишера можно заметить,  что основной  вклад дают точки, где  классификатор неуверен, а $\|F\|$ - отражает сложность задачи

Для сравнения эмбеддингов предлагаются 3 метрики

- $D (t_a \rightarrow t_b) = \frac{\mathbb{E}[t_{a} \rightarrow t_{b}] - \mathbb{E}[t_b]}{\mathbb{E}[t_b]}$
- $d_{sym}(F_a, F_b)  = d_{\cos}\left(\frac{F_a}{F_a+F_b}, \frac{F_a}{F_a + F_b} \right)$
- $d_{asym} = d_{sym}(t_a, t_b) - \alpha d_{sym}(t_a, t_0)$

Для учета роли модели в определении taskvec они параметризуют  представление таски как $t = F + m$, где $m$ - обучаемое представление модели, которое получается после решения следующей задачи:
$$
\mathcal{L}=\mathbb{E}\left[-\log p\left(m \mid d_{\mathrm{asym}}\left(t, m_{0}\right), \ldots, d_{\mathrm{asym}}\left(t, m_{k}\right)\right)\right]
$$

Эксперименты:
![[Pasted image 20211208184936.png]]

Для экспериментов использовались датасеты iNaturalist, iMaterialist, CUB-2000