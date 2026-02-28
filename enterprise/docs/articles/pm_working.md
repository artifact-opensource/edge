# Perceptual Manifolds: Workbook

## A Practical Guide to Understanding Semantic Compression

---

### Introduction to This Workbook

This workbook is designed to help you understand and apply the concepts of perceptual quantization and semantic compression. Each section includes:
- **Core Concepts**: Essential theory you need to know
- **Exercises**: Hands-on problems to solidify understanding
- **Reflection Questions**: Prompts to think deeper about implications
- **Code Challenges**: Implementation exercises where applicable

---

## Module 1: Information Theory Foundations

### Core Concepts

**Shannon vs. Kolmogorov: Two Ways to Measure Information**

- **Shannon Information**: Focuses on *statistical properties* of a source
  - Measures average uncertainty (entropy)
  - Best for known, repeating sources
  - Example: Compressing a text file where letter frequencies are known

- **Kolmogorov Complexity**: Focuses on the *individual object*
  - Measures the shortest program that can reproduce the data
  - Captures "intrinsic" complexity
  - Example: A truly random sequence vs. a pseudorandom one

### Exercise 1.1: Calculating Shannon Entropy

Given the probability distribution for a message source:
- Symbol A: p = 0.5
- Symbol B: p = 0.25
- Symbol C: p = 0.125
- Symbol D: p = 0.125

**Task**: Calculate the Shannon entropy H(X) = -Σ p(x) log₂ p(x)

**Your Work**:
```
H(X) = -(0.5 × log₂(0.5) + 0.25 × log₂(0.25) + 0.125 × log₂(0.125) + 0.125 × log₂(0.125))
     = -(0.5 × (-1) + 0.25 × (-2) + 0.125 × (-3) + 0.125 × (-3))
     = -(-0.5 - 0.5 - 0.375 - 0.375)
     = 1.75 bits per symbol
```

### Reflection Question 1.1

*Why might Shannon entropy fail to capture the "true" information content of a sequence like "ABABABABAB..." compared to a truly random sequence with the same letter frequencies?*

**Notes**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Exercise 1.2: Effectiveness Information

Consider these three datasets, all with the same Shannon entropy:
1. Raw sensor noise from a camera
2. A medical imaging scan with tumor indicators
3. Random stock price movements

**Task**: Rank these by "effectiveness information" for the task of medical diagnosis. Explain your reasoning.

**Your Answer**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Module 2: Scalar to Vector Quantization

### Core Concepts

**Lloyd-Max Quantizer: The Optimal Scalar Quantizer**

Two conditions for optimality:
1. **Centroid Condition**: Reconstruction level = mean of decision region
2. **Nearest-Neighbor Condition**: Decision boundary = midpoint between levels

**Why It Matters**: These conditions are coupled—changing thresholds affects optimal centroids and vice versa. This requires iterative algorithms.

### Exercise 2.1: Lloyd-Max Algorithm

Given a uniform distribution U[0, 1] and 4 quantization levels:

**Initial Setup**:
- Thresholds: t = [0, 0.25, 0.5, 0.75, 1.0]
- Levels: y = [?, ?, ?, ?]

**Task**: Calculate the optimal reconstruction levels y₁, y₂, y₃, y₄ using the centroid condition.

**Your Work**:
```
For uniform distribution on [a, b], E[X] = (a + b) / 2

y₁ = E[X | 0 ≤ X < 0.25] = (0 + 0.25) / 2 = 0.125
y₂ = E[X | 0.25 ≤ X < 0.5] = __________
y₃ = E[X | 0.5 ≤ X < 0.75] = __________
y₄ = E[X | 0.75 ≤ X < 1.0] = __________
```

### Exercise 2.2: Vector Quantization Gain

**Thought Experiment**: Why does a hexagonal lattice in 2D achieve lower distortion than a square grid for the same number of bits?

**Hint**: Think about how circles pack into hexagons vs. squares.

**Your Explanation**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Coding Challenge 2.1: Implement Simple Scalar Quantizer

```python
import numpy as np

def scalar_quantize(signal, num_levels):
    """
    Quantize a signal using uniform scalar quantization.
    
    Args:
        signal: numpy array of values in [0, 1]
        num_levels: number of quantization levels
    
    Returns:
        quantized signal and MSE
    """
    # TODO: Implement this function
    # Step 1: Determine thresholds
    # Step 2: Determine reconstruction levels
    # Step 3: Map each sample to nearest level
    # Step 4: Calculate MSE
    
    pass

# Test your implementation
test_signal = np.random.uniform(0, 1, 1000)
quantized, mse = scalar_quantize(test_signal, 16)
print(f"MSE: {mse}")
```

---

## Module 3: Perceptual Quantization

### Core Concepts

**The Perceptual Shift**: From pixel error to perceptual error

Traditional metrics like MSE assume all pixel changes are equally noticeable. The Human Visual System (HVS) doesn't work that way:
- More sensitive to contrast changes in smooth areas
- Less sensitive to noise in textured regions (masking)
- Highly sensitive to structural distortions

**Perceptual Vector Quantization (PVQ)**: Separates vectors into:
- **Gain** (energy/contrast): Quantized coarsely
- **Shape** (direction): Quantized finely

### Exercise 3.1: Contrast Masking

You have a video frame with two regions:
- Region A: Smooth gradient (low texture)
- Region B: Complex foliage (high texture)

With a fixed bit budget, should you allocate more bits to A or B? Why?

**Your Answer**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Exercise 3.2: Householder Reflection

Given prediction vector r = [3, 4] (length 5), we want to reflect an input vector x = [5, 0] so it aligns with r.

**Task**: Calculate the angle θ between x and r.

**Your Work**:
```
cos θ = (x · r) / (‖x‖ ‖r‖)
      = ((5×3) + (0×4)) / (5 × 5)
      = 15 / 25
      = 0.6

θ = arccos(0.6) ≈ 53.13°
```

### Reflection Question 3.1

*Film grain and noise can actually enhance perceived quality. Why might removing ALL high-frequency components make an image look "fake" or "plastic"?*

**Notes**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Module 4: Semantic Rate-Distortion

### Core Concepts

**Classical Rate-Distortion**:
```
R(D) = min I(X; X̂)  subject to  E[d(X, X̂)] ≤ D
```

**Semantic Rate-Distortion**:
```
R_s(D) = min I(X; Ẑ)  subject to  E[ℒ_s(X, D(Ẑ, M))] ≤ D
```

Key differences:
- Uses latent representation Ẑ instead of direct reconstruction
- Decoder has memory M (generative model)
- Distortion ℒ_s includes task loss, perceptual surprise, prediction error

### Exercise 4.1: Task-Aware Distortion

Consider compressing an image for two different tasks:
1. Human viewing on a display
2. Object detection by a neural network

The compression introduces artifacts that:
- Make the image slightly blurry to humans
- But preserve sharp edges around objects

**Task**: For each observer, determine if distortion is high or low. Explain.

**Your Answer**:
- Human observer: Distortion is _____ because _____________________
- Machine observer: Distortion is _____ because _____________________

### Exercise 4.2: Prediction Error

A video codec predicts the next frame will show a ball at position (100, 200). The actual ball is at (105, 203).

**Task**: Calculate the prediction error ‖x̂ₜ₊₁ - xₜ₊₁‖.

**Your Work**:
```
Error = √[(105-100)² + (203-200)²]
      = √[25 + 9]
      = √34
      ≈ 5.83 pixels
```

### Coding Challenge 4.1: Implement VQ-VAE Quantizer

```python
import torch
import torch.nn as nn

class SimpleVectorQuantizer(nn.Module):
    def __init__(self, num_embeddings=512, embedding_dim=64):
        super().__init__()
        # TODO: Initialize embedding codebook
        # Hint: Use nn.Embedding
        pass
    
    def forward(self, z):
        # TODO: Implement vector quantization
        # 1. Flatten spatial dimensions
        # 2. Calculate distances to all codebook vectors
        # 3. Find nearest codebook entry for each input vector
        # 4. Return quantized output
        pass

# Test
vq = SimpleVectorQuantizer()
dummy_input = torch.randn(4, 64, 8, 8)  # Batch, Channels, Height, Width
# quantized = vq(dummy_input)
```

---

## Module 5: Riemannian Quantization

### Core Concepts

**The Manifold Perspective**: Neural network parameters don't live in flat Euclidean space. They live on a curved manifold where some directions are more "important" than others.

**Fisher Information Matrix (FIM)**: Describes the local curvature of the parameter manifold
- High curvature = sensitive direction (small changes → big output changes)
- Low curvature = insensitive direction (changes don't matter much)

**RSAVQ Strategy**: 
- Allocate more bits to high-curvature channels
- Project quantization errors into low-curvature directions

### Exercise 5.1: Geometric Intuition

Imagine walking on a mountain (high curvature) vs. a flat plain (low curvature).

**Question**: If you can only take 10 steps total and want to minimize altitude change, should you take more steps on the mountain or the plain?

**Your Answer**:
_________________________________________________________________

**Application to Quantization**:
_________________________________________________________________
_________________________________________________________________

### Exercise 5.2: Fisher Information

Given a simple model y = wx where w is the parameter:
- For input distribution x ~ N(0, σ²)
- Fisher Information I = E[(∂log p/∂w)²]

**Task**: Explain intuitively why larger σ² means quantizing w is less sensitive.

**Your Explanation**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Module 6: Temporal Coding and the Time-Domain Brain

### Core Concepts

**Traditional Video Compression**: Stores motion vectors (how blocks moved)

**Future Paradigm**: Stores semantic state changes (what changed in meaning)

**Time-Domain Brain Theory**: Brain encodes information in spike timing patterns, not just spike rates
- Memory = distributed temporal patterns
- Perception = predicting future spike patterns

### Exercise 6.1: Predictive Coding

A video shows a ball thrown upward. The codec knows physics.

**Scenario 1**: Ball follows expected parabolic path
**Scenario 2**: Ball suddenly changes direction (edit/special effect)

**Task**: For each scenario, estimate relative bitrate needed.

**Your Answer**:
- Scenario 1: _____ bits (because _________________________)
- Scenario 2: _____ bits (because _________________________)

### Exercise 6.2: Event-Based Vision

Traditional cameras capture frames at fixed intervals (30 fps).
Event cameras trigger only when brightness changes.

**Task**: Describe a scene where event cameras would use drastically fewer "events" than frame cameras use pixels.

**Your Scene Description**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Reflection Question 6.1

*If a decoder has a perfect generative model of a scene, how many bits theoretically needed to transmit a predictable video sequence?*

**Your Thoughts**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Module 7: Machine Vision and VCM

### Core Concepts

**Video Coding for Machines (VCM)**: Optimizes compression for machine vision tasks
- Traditional codecs optimize for human perception
- VCM optimizes for task accuracy (detection, tracking, classification)

**Satisfied Machine Ratio (SMR)**: Proportion of machines that achieve acceptable task performance on compressed data
- Different machines = different sensitivities
- Optimizing for one machine may hurt another

### Exercise 7.1: Human vs. Machine Perception

Consider compression artifacts that:
- Blur license plate numbers slightly (humans barely notice)
- Preserve overall scene structure

**Task**: Compare impact on two tasks:
1. Human: Enjoying a TV show
2. Machine: License plate recognition

**Your Analysis**:
- Human impact: _______________________________________________
- Machine impact: ______________________________________________

### Exercise 7.2: ROI (Region of Interest) Coding

An autonomous driving camera compresses video with:
- High quality for road/cars (ROI)
- Low quality for sky/trees (non-ROI)

**Task**: Calculate total bitrate if:
- ROI is 30% of pixels at 10 bits/pixel
- Non-ROI is 70% of pixels at 2 bits/pixel

**Your Work**:
```
Average bitrate = (0.30 × 10) + (0.70 × 2)
                = 3.0 + 1.4
                = 4.4 bits/pixel
```

### Design Challenge 7.1

Design a compression scheme for a security camera system where:
- Most footage shows empty hallways (boring)
- Rare footage shows people/activity (important)

**Your Design**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Module 8: Hardware and Energy Constraints

### Core Concepts

**The Energy Crisis**: Neural codecs can be 800× more expensive than image generation
- Limits deployment on mobile/edge devices
- Requires hardware-aware optimization

**Solutions**:
- GIC-DLC: Uses logic gates instead of floating-point ops
- Quantization: 8-bit, 4-bit, or even 2-bit integer representations
- ARM optimizations: NEON SIMD instructions

### Exercise 8.1: Energy Analysis

A smartphone has 3000 mAh battery at 3.7V = 11.1 Wh total energy.

**Scenario**: Neural video decoder uses 1 W continuous power.

**Task**: How many hours of video can be decoded?

**Your Work**:
```
Time = Energy / Power
     = 11.1 Wh / 1 W
     = 11.1 hours
```

Now if optimization reduces power to 0.2 W:
```
New time = 11.1 / 0.2 = _____ hours
```

### Exercise 8.2: Quantization Trade-offs

| Precision | Model Size | Accuracy | Inference Speed |
|-----------|------------|----------|-----------------|
| FP32 | 1.0× | 95.2% | 1.0× |
| INT8 | 0.25× | 94.8% | 3.5× |
| INT4 | 0.125× | 92.1% | 7.2× |

**Task**: For a mobile deployment where speed matters most but accuracy must stay above 93%, which precision would you choose?

**Your Choice**: ___________

**Justification**:
_________________________________________________________________
_________________________________________________________________

---

## Module 9: Privacy and Regulatory Challenges

### Core Concepts

**Personalized Compression**: Uses eye-tracking to allocate bits where you're looking
- Can save 30-50% bitrate
- But eye movement data is biometric and sensitive

**Regulatory Landscape**:
- GDPR: Requires consent for biometric profiling
- EU AI Act: Prohibits certain biometric categorization
- Privacy by Design: Build privacy into the system, not bolt it on

### Exercise 9.1: Privacy-Preserving Saliency

A video codec wants to use gaze tracking without storing eye positions.

**Task**: Design a privacy-preserving approach using Differential Privacy.

**Your Design Sketch**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Reflection Question 9.1

*If saliency models are trained on predominantly Western datasets, how might they fail for users from different cultural backgrounds?*

**Your Thoughts**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Case Study 9.1

Company X builds VR headsets with built-in eye tracking. They use it for:
1. Foveated rendering (technical optimization)
2. Attention analytics (which ads users look at)

**Task**: Identify potential GDPR violations and propose solutions.

**Your Analysis**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Module 10: Synthesis and Future Directions

### Reflection Question 10.1

*"Compression is coordination, not preservation." What does this mean for the future of communication systems?*

**Your Extended Thoughts**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Exercise 10.1: Falsifiable Predictions

The main text makes several predictions for 2025-2035:
1. Motion vectors will disappear
2. Bitstreams will become latent programs
3. Pixel-fidelity metrics will be abandoned
4. Decoder size will dominate
5. Closed-loop personalization will succeed

**Task**: For each prediction, describe what evidence would falsify it.

**Prediction 1 - Falsification Test**:
_________________________________________________________________

**Prediction 2 - Falsification Test**:
_________________________________________________________________

**Prediction 3 - Falsification Test**:
_________________________________________________________________

### Final Project: Design Your Own Semantic Codec

**Scenario**: Design a compression system for a specific use case of your choice.

**Your Use Case**:
_________________________________________________________________

**Design Requirements**:
1. What is being compressed? (image, video, 3D, etc.)
2. Who/what is the observer? (human, machine, both)
3. What is the task? (viewing, detection, reconstruction)
4. What are the constraints? (bandwidth, latency, energy, privacy)

**Your Design**:

**Architecture**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Quantization Strategy**:
_________________________________________________________________
_________________________________________________________________

**Perceptual Model**:
_________________________________________________________________
_________________________________________________________________

**Novelty / Key Innovation**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Expected Performance**:
- Compression ratio: __________
- Quality metric: __________
- Constraints satisfied: __________

---

## Appendix A: Mathematical Proofs Workthrough

### Proof 1: Lloyd-Max Centroid Condition

**Given**: Distortion D_k = ∫[t_k to t_{k+1}] (x - y_k)² f_X(x) dx

**Goal**: Show that optimal y_k = E[X | t_k ≤ X < t_{k+1}]

**Your Step-by-Step Proof**:

Step 1: Take derivative with respect to y_k
```
∂D_k/∂y_k = ∫[t_k to t_{k+1}] _____________ dx
```

Step 2: Set equal to zero and solve
```
_________________________________________________________________
```

Step 3: Interpret the result
```
_________________________________________________________________
```

### Proof 2: Householder Reflection Preserves Norm

**Claim**: If H = I - 2uuᵀ where ‖u‖ = 1, then ‖Hx‖ = ‖x‖ for any x

**Your Proof**:
```
‖Hx‖² = (Hx)ᵀ(Hx)
      = xᵀHᵀHx
      
First, show that Hᵀ = H (H is symmetric):
_________________________________________________________________

Then, show that H² = I (H is an involution):
_________________________________________________________________

Therefore:
‖Hx‖² = xᵀHx = ___________________________________________
```

---

## Appendix B: Code Templates

### Template 1: Saliency Map Generation

```python
import torch
import torchvision.models as models

class SimpleSaliencyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # TODO: Design architecture
        # Hint: Use a CNN encoder + attention mechanism
        pass
    
    def forward(self, image):
        # TODO: Return saliency map [0, 1] for each pixel
        # Higher values = more salient
        pass

# Usage
model = SimpleSaliencyModel()
# saliency = model(input_image)
```

### Template 2: Rate-Distortion Optimization

```python
def optimize_bit_allocation(image, target_rate, saliency_map):
    """
    Allocate bits across image regions based on saliency.
    
    Args:
        image: Input image
        target_rate: Total bit budget
        saliency_map: Importance map [0, 1]
    
    Returns:
        bit_allocation: Bits per pixel for each region
    """
    # TODO: Implement Lagrangian optimization
    # Hint: High saliency → more bits
    pass
```

---

## Appendix C: Additional Resources

### Recommended Reading
1. Cover & Thomas: "Elements of Information Theory"
2. Kolmogorov: "Three Approaches to Information"
3. Shannon: "A Mathematical Theory of Communication"
4. Recent VQ-VAE and semantic compression papers

### Online Resources
- Stanford EE269 (Compression & Coding)
- Daala/Opus codec documentation
- PyTorch VQ-VAE tutorials

### Datasets for Practice
- Kodak image dataset (standard benchmark)
- ImageNet (large-scale)
- WIC640 (saliency with demographics)

---

## Your Learning Journey: Reflection

### What concepts were most challenging?
_________________________________________________________________
_________________________________________________________________

### What connections did you make to other fields?
_________________________________________________________________
_________________________________________________________________

### What questions remain unanswered?
_________________________________________________________________
_________________________________________________________________

### How might you apply these ideas?
_________________________________________________________________
_________________________________________________________________

---

**End of Workbook**

*Remember: The goal is not just to compress signals, but to understand and coordinate meaning across systems. Every bit should serve a purpose, every quantization should respect the geometry of perception.*
