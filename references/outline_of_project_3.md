# 3. Introduction to Gaussian Mixture Models (GMM)

Gaussian Mixture Models (GMM) are an essential tool in unsupervised machine learning, particularly for applications where clusters overlap and transitions between categories are gradual rather than discrete. In plasma physics, and particularly in MMS data analysis, plasma populations are often continuously distributed rather than sharply separated. Traditional clustering techniques, such as k-Means, assume that each data point belongs to a single, well-defined cluster, but in reality, plasma transitions can be gradual and complex.

## Why GMM is Well-Suited for Plasma Analysis

1. Soft Clustering for Continuous Transitions: Instead of rigidly assigning data points to a single group, GMM allows for probabilistic classification, meaning that each plasma observation has a probability of belonging to multiple clusters.
2. Uncertainty Estimation: Unlike threshold-based classification, which forces hard decisions, GMM provides an uncertainty measure, which is crucial for analyzing plasma populations that transition gradually between different regimes.
3. Handling Non-Spherical Distributions: Unlike k-Means clustering, which assumes circular (spherical) clusters, GMM can model elliptical distributions, making it better suited for anisotropic plasma structures.

## Brief Theoretical Background

GMM is a type of probabilistic model that assumes the dataset can be represented as a mixture of multiple Gaussian (normal) distributions. Each Gaussian component represents a different underlying population, and the overall model estimates the probability that a given data point belongs to each of these populations.
1. Each data point belongs to multiple clusters with a certain probability rather than being assigned to just one cluster.
2. The goal of GMM is to learn the underlying parameters of these Gaussian distributions, including mean, variance (covariance), and mixing proportions.

### Mathematical Formulation

GMM models a dataset as a sum of multiple Gaussian distributions:

$$ P(x) = \sum_{i=1}^{K} w_i \cdot \mathcal{N}(x | \mu_i, \Sigma_i) $$

where:
- $K$ is the number of clusters (Gaussian components)
- $w_i$ represents the weight (mixing coefficient) of each Gaussian
- $\mu_i$ and $\Sigma_i$ are the mean vector and covariance matrix of each Gaussian component
- $\mathcal{N}(x | \mu_i, \Sigma_i)$ is the Gaussian probability density function

### Expectation-Maximization (EM) Algorithm

GMM parameters are learned using the Expectation-Maximization (EM) algorithm, an iterative method that finds the best-fitting Gaussian distributions for the dataset.

#### Steps of EM Algorithm
1. E-step (Expectation Step): Compute the probability that each data point belongs to each Gaussian component.
2. M-step (Maximization Step): Update the Gaussian parameters (means, covariances, and mixing weights) based on the probabilities computed in the E-step.

This process repeats until convergence, meaning that the parameters no longer change significantly between iterations.

| Feature | k-Means | GMM |
|---------|---------|-----|
| Clustering Type | Hard (Each point assigned to one cluster) | Soft (Each point has probabilities for multiple clusters) |
| Shape of Clusters | Spherical | Elliptical |
| Probability Estimation | No | Yes |
| Handles Overlapping Data | No | Yes |
| Works for Complex Plasma Distributions | No | Yes |

## Numerical Implementation

### Choosing the Number of Clusters (K)

Determining the optimal number of clusters is a crucial step in GMM. Common methods include:
- Bayesian Information Criterion (BIC) and Akaike Information Criterion (AIC): These statistical criteria help penalize overly complex models and prevent overfitting.
- Elbow Method: Evaluates model performance across different values of  K  and selects the point where improvements start to level off.

### Covariance Structure in GMM

The covariance structure determines the shape of the Gaussian clusters:
- Full – Each cluster has its own covariance matrix (flexible but computationally expensive).
- Tied – All clusters share the same covariance matrix (reduces complexity).
- Diagonal – Each cluster has a diagonal covariance matrix (restricts relationships between features but is computationally efficient).

### Handling High-Dimensional Feature Spaces

MMS data contains multiple plasma parameters (e.g., density, velocity, turbulence metrics). In high-dimensional spaces, GMM clustering can be enhanced by dimensionality reduction techniques such as Principal Component Analysis (PCA).

## Challenges in Applying GMM to MMS Data

While GMM is a powerful clustering method, applying it to MMS plasma data presents additional challenges:

1. Plasma Data is Multi-Dimensional
   - Unlike the 2D toy model, real MMS data involves multiple plasma features
   - Selecting the most relevant features is crucial to achieving meaningful classification

2. Complex Covariance Structures in Plasma Populations
   - Plasma populations are often anisotropic and influenced by turbulence
   - Advanced modeling techniques, such as hierarchical GMM or Bayesian GMM, may improve classification

3. Feature Engineering for Plasma Classification
   - Many plasma characteristics are not directly measured but need to be derived
   - Additional feature engineering, such as turbulence spectral analysis, may improve GMM classification accuracy