import matplotlib.pyplot as plt
import random




num_days = 30
days = range(num_days)
y_pos = range(len(days))
performance = [
    random.randint(0,40) for _ in range(num_days)
]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, days)
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()