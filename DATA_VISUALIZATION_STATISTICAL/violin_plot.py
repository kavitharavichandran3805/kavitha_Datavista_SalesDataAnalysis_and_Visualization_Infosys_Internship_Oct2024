# Import necessary libraries
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Iris dataset
data = sns.load_dataset("iris")

# Set the figure size
plt.figure(figsize=(10, 6))

# Create a violin plot for petal length by species
sns.violinplot(data=data, x="species", y="petal_length", palette="Pastel1", inner="quartile")

# Add titles and labels
plt.title("Violin Plot of Petal Length by Species")
plt.xlabel("Species")
plt.ylabel("Petal Length (cm)")
plt.savefig("violin_plot.png", format="png", dpi=300)
# Show the plot
plt.show()
