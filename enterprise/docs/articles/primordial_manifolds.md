# Primordial Manifolds: The Paradigmatic Convergence of Signal, Meaning, and Consciousness

---

## Thesis: From Signal Compression to Semantic Execution

Compression is no longer the problem of reproducing signals under bandwidth constraints. It is the problem of inducing equivalent meaning, perception, and task performance in a system that already possesses memory, priors, and predictive models.

Classical information theory optimized bits per symbol and treated distortion as waveform error. This assumption fails in high-dimensional, semantically structured media, where most signal content is predictable, inferable, or irrelevant to the observer's objectives. Semantic Rate–Distortion theory formalizes this shift by redefining distortion in terms of task loss, perceptual surprise, and prediction error rather than pixel deviation.

Under this framework, optimal compression does not transmit signals but activates models. Bitstreams cease to be descriptions of data and instead become compact control codes that trigger generative reconstruction conditioned on shared priors. The efficiency frontier is therefore governed not by transform efficiency but by alignment between encoder outputs and decoder world models.

The inevitable consequence is a paradigmatic transition: motion vectors yield to latent state propagation, codecs evolve into executable semantic programs, decoder complexity dominates system design, and fidelity is measured by indistinguishability of meaning rather than equality of samples.

Compression thus converges with inference. Transmission becomes coordination. The signal is no longer preserved—it is reconstructed by understanding.

---

## A Modern Synthesis of Signal, Manifold, and Meaning

The trajectory of information theory and data compression has reached a critical juncture where classical signal-processing techniques, once sufficient for low-fidelity transmission, can no longer meet the demands of high-dimensional, semantically-rich media. For decades, the industry relied on the mathematical foundations laid by Claude Shannon, focusing primarily on the reduction of statistical redundancy within raw waveforms. 

However, the contemporary landscape is defined by a transition toward structured, perceptual, and latent quantization paradigms. This evolution is characterized by a move from independent scalar operations to manifold-aware vector quantization, from signal-space error minimization to perceptual-space fidelity, and from open-loop fixed curves to closed-loop, environment-aware systems. 

Furthermore, the rise of neural latent quantization and event-based temporal modeling suggests a future where bits are allocated based on meaning rather than amplitude, and where the compression architecture accounts for the prior knowledge and physiological characteristics of the human observer. This is not merely an engineering refinement—it represents a philosophical transformation in our understanding of what information is and how it should be measured.

---

## I. Historical Foundations: The Shannon-Kolmogorov Duality

The intellectual history of data compression is rooted in two distinct but complementary definitions of information. Shannon's information theory, established in 1948, is fundamentally concerned with the communication process. It defines information in terms of a random source, focusing on the minimum expected number of bits required to transmit a message through an error-free channel. Shannon entropy measures the average uncertainty or surprise associated with a set of possible outcomes, effectively quantifying the limits of lossless compression based on the statistical properties of the source. This approach assumes that the characteristics of the random source are known and that the goal is to optimize the transmission of messages from that source.

In contrast, Algorithmic Information Theory, pioneered in the 1960s by Solomonoff, Kolmogorov, and Chaitin, focuses on the individual object itself rather than the probabilistic source. Kolmogorov complexity (K) measures the length of the shortest computer program that can reproduce a specific sequence of data and then halt. While Shannon entropy ignores the specific content of a message to focus on its probability, Kolmogorov complexity treats the data as a unique entity whose complexity is defined by its inherent patterns and structural regularities. 

This distinction is critical for modern semantic compression: whereas Shannon provides the bounds for transmitting "data," Kolmogorov provides the theoretical threshold for capturing "meaning". The relationship between these theories is best illustrated through universal coding, which serves as a middle ground. While Shannon's approach is limited by the need to know the source's characteristics beforehand, Kolmogorov's approach is lower-semi-computable, meaning the absolute shortest program cannot be found by a universal algorithm. Nevertheless, approximations of Kolmogorov complexity, often through the use of sophisticated compression algorithms or algorithmic probability, allow for the identification of "meaningful information" in datasets that look random to purely statistical (Shannon-based) estimators.

### The Three Pillars of Information

| Information Pillar | Core Metric | Primary Focus | Practical Constraint |
|-------------------|-------------|---------------|---------------------|
| Shannon Information | Entropy (H) | Random source statistics | Requires known source properties |
| Algorithmic Theory | Kolmogorov Complexity (K) | Individual object description | Theoretically non-computable |
| Logical Depth | Computation Time | Structural complexity | Measures generation effort |
| Effectiveness Information | Semantic Value | Task-specific utility | Context-dependent |

The concept of "effectiveness information" introduces a third dimension beyond statistical and algorithmic complexity. Grounded in the work of Luciano Floridi, this paradigm suggests that information is not merely a measure of uncertainty or program length, but a function of its utility in a task-oriented environment. In this framework, information quality is measured by its accuracy, completeness, relevancy, and interpretability, all of which influence the effectiveness of decision-making. This transition from signal to semantics is the driving force behind the contemporary shift in quantization research.

---

## II. Redefining Information: Semantic Rate–Distortion Theory (SRD)

The most fundamental shift in the current landscape is the explicit redefinition of "information." While Shannon optimized bits per symbol, modern Semantic Rate–Distortion (SRD) theory optimizes bits per meaning. Classical rate–distortion theory defines distortion as an expected signal-space error, typically mean squared error (MSE) between an original waveform x and its reconstruction x̂. This assumes all deviations are equally meaningful, an assumption that fails for perceptual and task-driven media.

### The Formal Regimes of SRD

We define the Semantic Rate-Distortion function as:

**R_s(D) = min_{p(ẑ|x)} I(x; ẑ) subject to E[ℒ_s(x, D(ẑ, M))] ≤ D**

Where:
- ẑ is a quantized latent representation
- x̂ is the reconstruction produced by a generative decoder with memory M
- ℒ_s is a semantic distortion functional, rather than a pixel metric

Semantic distortion decomposes into three orthogonal terms:

1. **Task Loss (ℒ_task)**: Measures degradation in downstream utility (e.g., classification accuracy). If the task outcome is unchanged, distortion is zero, regardless of pixel variance.

2. **Perceptual Surprise (ℒ_surprise)**: Quantifies deviation from expected perceptual statistics under the observer's internal model:
   ```
   ℒ_surprise ∝ -log p(x̂ | context, memory)
   ```

3. **Prediction Error (ℒ_prediction)**: Measures the mismatch between predicted and observed future states:
   ```
   ℒ_prediction = ‖x̂_{t+1} - E[x_{t+1} | x_{≤t}]‖
   ```

This reformulation has profound implications. It suggests that the "correct" amount of compression depends not on the signal's statistical properties alone, but on the cognitive architecture of the observer and the purpose for which the information will be used. In essence, we are moving from a theory of communication to a theory of coordination.

---

## III. Structural Evolution: From Scalar to Riemannian Quantization

### The Mathematical Constraints of Scalar Paradigms (Engineering Reality)

The fundamental unit of lossy compression, the quantizer, has undergone a profound structural transformation. Early digital systems utilized scalar quantization (SQ), where each individual sample—whether a pixel intensity or an audio pulse—was mapped independently to the nearest discrete level. While SQ is computationally efficient and easily implemented in hardware, it is inherently limited because it treats multi-dimensional data as a collection of isolated points, thereby failing to exploit the intrinsic structural correlations present in natural signals.

Scalar quantization operates on the premise of minimizing the mean square error (MSE) for a single dimension. The Lloyd-Max quantizer remains the gold standard for this approach, characterized by a set of boundary points t_k and reconstruction levels y_k that satisfy two necessary conditions for local optimality.

**Workout: Proof of the Centroid Condition (C1)**

The objective is to minimize total distortion D for a fixed set of decision thresholds {t_k}. The distortion in each cell k is:

```
D_k = ∫_{t_k}^{t_{k+1}} (x - y_k)² f_X(x) dx
```

Differentiating D_k with respect to the reconstruction level y_k:

```
∂D_k/∂y_k = -2 ∫_{t_k}^{t_{k+1}} (x - y_k) f_X(x) dx = 0
```

Solving for y_k:

```
y_k = ∫_{t_k}^{t_{k+1}} x f_X(x) dx / ∫_{t_k}^{t_{k+1}} f_X(x) dx = E[X | t_k ≤ X < t_{k+1}]
```

Thus, the optimal reconstruction level is the centroid of the decision region. This ensures that for any given set of thresholds, the reconstruction levels minimize the distortion within each cell.

**Workout: Proof of the Nearest-Neighbor Condition (C2)**

Optimizing thresholds {t_k} for fixed y_k. An interior boundary t_k affects the sum D_{k-1} + D_k. Differentiating with respect to t_k using Leibniz' rule and assuming f_X(t_k) > 0:

```
∂(D_{k-1} + D_k)/∂t_k = (t_k - y_{k-1})² f_X(t_k) - (t_k - y_k)² f_X(t_k) = 0
```

Thus:

```
t_k = (y_{k-1} + y_k) / 2
```

The optimal threshold is the exact midpoint between reconstruction levels. These conditions are implicit and coupled, usually requiring an iterative algorithm for numerical design since closed-form solutions are rare for complex probability density functions.

Despite these optimizations, scalar quantization fails to exploit the "space-filling gain" available in higher dimensions. Research into lattice quantization and vector quantization (VQ) demonstrates that partitioning a multi-dimensional space into more complex shapes (such as hexagonal lattices in 2D or E8 lattices in 8D) achieves a lower average distortion for a given number of bits. VQ achieves this by mapping blocks of data to a finite set of representative vectors in a codebook, capturing the global density of the data distribution rather than local sample amplitudes.

### Riemannian Sensitivity and Information Geometry (Research Frontier)

The transition toward Large Language Models (LLMs) and deep neural networks has introduced a new challenge: the parameters of these models do not reside in a flat Euclidean space but on a Riemannian manifold with non-uniform curvature. Traditional post-training quantization (PTQ) methods that assume Euclidean geometry often lead to "unconstrained direction error," where the quantization noise significantly shifts the model's output in sensitive directions.

The Riemannian Sensitivity-Aware Vector Quantization (RSAVQ) framework addresses this by leveraging information geometry to model the parameter space. By utilizing the Fisher Information Matrix (FIM), RSAVQ characterizes the local geometric structure, including inter-parameter correlations and manifold curvature. This allows for the implementation of Error Direction Sensitivity Guidance (EDSG), which projects quantization errors onto low-sensitivity directions—specifically along the negative natural gradient directions on the manifold.

The mathematical justification for this approach lies in the Fisher-weighted sensitivity metric:

```
I_c = ‖F_c^{1/2} ∇L_c‖²
```

Where ∇L_c is the gradient of the loss function with respect to the c-th channel and F_c is the corresponding FIM block. By allocating more bits to channels with high curvature (high I_c) and projecting errors in less critical channels into "null spaces" of the loss function, RSAVQ preserves model accuracy even at extremely low bitrates of 2 to 4 bits.

This represents a philosophical shift: quantization is no longer a purely mechanical process of rounding numbers but a geometric operation that respects the intrinsic structure of the information space. The quantizer must "understand" the manifold on which the data lives.

### Comparative Taxonomy of Quantization Paradigms

| Quantization Level | Geometric Assumption | Error Model | Awareness |
|-------------------|---------------------|-------------|-----------|
| Standard Scalar (SQ) | Flat Euclidean (1D) | Isotropic / Midpoint | Independent samples |
| Standard Vector (VQ) | Flat Euclidean (ND) | Voronoi Tesselation | Structural correlations |
| RSAVQ (Riemannian) | Curved Manifold | Natural Gradient Projection | Curvature & Sensitivity |
| Polar PCDVQ | Polar Coordinates | Radial/Angular Decoupling | Energy-Shape awareness |

---

## IV. Perceptual Quantization: Appearance and Primitives

The philosophical core of modern compression is the shift from signal space to perceptual space: the goal is no longer the reconstruction of exact pixel values, but the preservation of the visual experience. This requires a move away from generic error metrics like Mean Squared Error (MSE) toward models that understand human visual system (HVS) characteristics such as contrast, texture, and structural integrity.

### Perceptual Vector Quantization (PVQ) and Contrast Masking

A prominent implementation of this shift is the Perceptual Vector Quantization (PVQ) used in the Daala video codec and the Opus audio codec (via the CELT mode). PVQ is based on the "gain-shape" decomposition of a vector of transform coefficients. Instead of quantizing individual AC coefficients, PVQ treats them as a single vector and separates them into a length (gain) and a unit-norm direction (shape).

This separation is motivated by the observation that preserving the "energy" (contrast) of a block is more perceptually important than preserving its exact phase or amplitude details. By explicitly quantizing the gain, the codec can apply a "contrast masking" model where quantization noise is allowed to increase in areas of high contrast, following a power law such as α = 1/3. This "companding" ensures that bits are not wasted on details that are already masked by the human eye's inability to perceive fine noise in busy textures.

### Householder Reflections in Vector Prediction

A significant hurdle in vector-based prediction is that subtracting a predictor from a signal destroys the vector's energy properties, making energy-conserving quantization impossible. Daala solves this by using a Householder reflection to "rotate" the coordinate system so that the prediction vector aligns with one of the primary axes.

**Workout: Coordinate Rotation Logic**

Let r be the prediction vector. We construct a Householder reflection matrix H to transform r into a vector with only one non-zero component:

```
H = I - 2uuᵀ
```

where u is a unit normal for the plane across which the vector x is reflected. In Daala, a reflection plane is found that turns the prediction into a vector with only one non-zero component. The input vector x is reflected to a new vector z that preserves its norm while aligning its primary component with the predictor.

This allows the codec to signal the "match" between the input and the prediction using an angle θ:

```
cos θ = (zᵀr) / (‖z‖‖r‖)   [Position along prediction axis]
sin θ                        [Remaining energy]
```

This geometric approach maintains structural coherence that simple subtraction-based codecs lack. It preserves structural textures rather than low-passing them, saving 13.7% to 24.8% in bitrate while maintaining perceptual fidelity.

### Noise, Grain, and Material Perception

The HVS does not treat all high-frequency signals as noise. Film grain and texture are essential for a realistic appearance, and removing them results in a "waxy" or unnatural look. Modern codecs treat noise and grain as perceptual primitives—structured components that can be modeled using physics-based heteroscedastic noise models. By transmitting the "recipe" for these textures rather than the textures themselves, encoders can achieve extreme compression without losing the perceived fidelity of the material.

Material perception research indicates that the HVS is highly sensitive to the statistics of pixel-based and sub-band luminance histograms, particularly positive skewness associated with specular highlights. Codecs that preserve the spatial alignment of these highlights with object contours maintain the perceived realism of materials like wood or polished metal. This sensitivity is increasingly integrated into Perceptual Image Quality Assessment (PIQA) metrics, which move beyond pixel-wise comparison to evaluate contrast masking and structural integrity.

### Taxonomy of Compression Architectures

| Feature | Signal-Preserving (Shannon) | Model-Triggering (Semantic) |
|---------|----------------------------|----------------------------|
| Objective | Reconstruct raw waveforms | Reconstruct experience/meaning |
| Distortion | Pixel/Sample Error (MSE) | Semantic loss / Task utility |
| Decoder | Stateless / Lightweight | Heavy / Generative / Memory-bearing |
| Examples | JPEG, H.264, AV1 | VQ-VAE, VQGAN, DCVC-FM |
| Bitstream | "What the signal was" | "What to reconstruct" (Instructions) |

---

## V. Neural Latent Quantization and its Bottlenecks

The most significant jump in compression efficiency occurs with neural latent quantization. This paradigm involves training autoencoders to learn an optimal perceptual basis for a dataset, effectively mapping high-dimensional signals onto a lower-dimensional latent manifold.

### Autoencoders, VAE-VQ, and Codebook Activation

The core mechanism of neural latent quantization is the Variational AutoEncoder (VAE) and its discrete counterpart, the VQ-VAE. In these systems, an encoder maps the input signal x to a latent representation z, which is then quantized to a discrete codebook before being reconstructed by the decoder. This process ensures that "bits follow meaning" rather than raw amplitude. By measuring the likelihood loss in the latent space rather than the pixel space, the model avoids wasting capacity on imperceptible noise or high-entropy textures.

However, traditional VQ-based methods often suffer from "codebook collapse," where only a small subset of the codewords is utilized, leading to a loss of representational capacity. Modern frameworks address this by using Gaussian-distributed latent spaces and distribution consistency regularization to ensure that the semantic meaning of a latent vector is preserved through the quantization bottleneck.

### The Inference Energy Crisis

Training autoencoders maps high-dimensional signals onto a lower-dimensional latent manifold. However, this paradigm introduces significant costs:

- **Inference Energy Crisis**: AI inference consumes 80-90% of computing power. Video generation consumes nearly 1 kWh per 5-second clip—800x more than high-quality images.
- **Decoder Lock-in**: Semantic codecs require the decoder to share a massive generative "prior." If a "distribution shift" occurs (unseen test data), performance collapses.
- **Cross-Platform Inconsistency**: Floating-point rounding errors on different GPUs introduce reconstruction drift.

### Hardware-Aware Solutions: GIC-DLC and Logic Circuits

While neural image codecs achieve higher compression ratios than traditional hand-crafted methods like PNG or JPEG-XL, they often incur substantial computational overhead, limiting their deployment on energy-constrained devices. The emergence of GIC-DLC (Gated Information Compression via Differentiable Logic Circuits) offers a natural solution.

By replacing conventional floating-point networks with trainable lookup tables and logic gates, GIC-DLC achieves high compression efficiency while maintaining low-latency inference. This architecture operates closer to the hardware's native logic, reducing power consumption on smartphones and drones by avoiding unnecessary floating-point operations. Optimization for ARM architectures, such as the ncnn framework, further boosts performance by using NEON instructions for fast vectorized operations, ensuring that complex machine vision models can run without draining the device's battery.

| Inference Framework | Architecture Target | Key Optimization | Benefit |
|-------------------|-------------------|-----------------|---------|
| GIC-DLC | Logic Circuits / LUTs | Differentiable Logic | Low Power/Energy |
| ncnn | ARM (Mobile/Edge) | NEON Acceleration | 2x Throughput |
| TensorRT | NVIDIA GPU | Precision Calibration | Maximum Latency reduction |
| DCVC-FM | Neural Video | Hybrid INT Quantization | Theoretical Complexity reduction |

---

## VI. Personalization and the Regulatory Frontier

Closed-loop systems introduce feedback from the display and the observer. Personalized saliency bit allocation adjusts bits based on the individual's gaze. This introduces significant regulatory friction.

### Saliency-Predicted and Eye-Tracked Bit Allocation

The most effective way to save bits is to avoid quantizing what the viewer cannot see. Saliency prediction models, often based on deep learning and Transformer architectures, simulate the human attention mechanism. These models generate attention maps that predict the probability of a human observer fixating on specific regions of a scene. By allocating higher quantization precision to these foveal regions and drastically reducing the bitrate for the periphery, codecs can achieve significant gains in perceived quality.

State-of-the-art saliency models are evaluated using several metrics:

- **Similarity (SIM)**: Measures the distribution similarity by summing the minimum values at each pixel
- **Correlation Coefficient (CC)**: Measures the linear relationship between predicted and ground truth saliency maps
- **Normalized Scanpath Saliency (NSS)**: Measures saliency at fixation points
- **Kullback-Leibler Divergence (KLD)**: Measures information loss between distributions

The integration of high-speed, closed-loop eye-trackers like EyeLoop—operating at over 1,000 frames per second on consumer hardware—enables real-time display-aware quantization. This allows the system to adjust the quantization lattice dynamically based on the viewer's gaze, a technique vital for virtual reality and medical imaging.

### Regulatory Challenges: GDPR and the EU AI Act

Eye-tracking data is a sensitive biometric indicator. The regulatory environment around personalized compression is complex:

- **GDPR and Behavioral Profiling**: Irish regulators issued a €310M fine for profiling without consent
- **EU AI Act**: Prohibits AI systems that categorize persons based on biometric data to deduce sensitive traits
- **Privacy by Design**: Future standards must implement Privacy-Preserving Saliency, using Differential Privacy (calibrated noise in attention maps) or Homomorphic Encryption

### Demographic and Cultural Diversity in Perception

Research has uncovered that gaze behavior patterns vary significantly across demographics. For example, female-trained saliency models have shown different performance characteristics compared to male-trained models when evaluated on datasets like WIC640. Factors such as age and cultural background influence how individuals navigate visual scenes, implying that the "optimal" bit allocation for one user may be suboptimal for another. This level of personalization represents the frontier of closed-loop quantization, where the encoder-decoder-display loop incorporates the observer's profile as a primary input.

---

## VII. Temporal Redundancy Beyond Motion Vectors

Traditional video compression relies on motion estimation and motion compensation (MEMC) to remove inter-frame redundancy. However, motion vectors are limited by their inability to capture complex transformations and their reliance on handcrafted subtraction operations.

### Event-Based Vision and SATE

The emergence of event cameras—which provide asynchronous, low-latency visual signals based on brightness changes—offers a new perspective on temporal modeling. Frame-based paradigms are ill-suited for these streams. The Scale-Aware Temporal Encoding (SATE) framework introduces recurrent modules at lower spatial scales where events are most dense. SATE utilizes Decoupled Deformable-enhanced Recurrent Layers (DDRL) to model the inherent motion characteristics of event streams. This "divide-and-conquer" strategy decouples feature fusion from motion estimation, allowing the system to filter out noise while preserving fine-grained temporal cues.

### The Time-Domain Brain and Semantic Pointers

The theoretical frontier of temporal compression is the "Time-Domain Brain" theory, which posits that major brain functions are realized through circulating and propagating characteristic temporally patterned signals. In this framework, neural assemblies produce complex spike patterns for every attribute of an object or event. These spike patterns are mixed digital-analog signals where the continuous values of the durations between discrete events convey information.

Memory operates on holographic principles, where nonlocal, distributed temporal spike patterns encode the actual attributes—the "what"—of an event. For video compression, this implies that the encoder could leverage the viewer's internal "generative model" by sending only the "delta-saliency"—the change in perception rather than the change in pixels. If the viewer can predict the next sequence of frames based on prior knowledge (e.g., a ball falling according to gravity), those frames require significantly fewer bits.

The concept of spike-timing-dependent plasticity (STDP) suggests that neural circuits preserve and manipulate sensory information through the relative timing of spikes in the millisecond range. By integrating STDP-like mechanisms into the encoder-decoder loop, compression systems can develop a "temporary network" that supports long-term working memory of the video stream. This allows the decoder to maintain a high-fidelity representation of the scene's context, reducing the need for repeated transmission of static or predictable information.

---

## VIII. Video Coding for Machines (VCM) and Feature Standards

A fundamental shift in the "observer" is the rise of machines as the primary consumers of visual data. Traditional video coding standards (AVC, HEVC, VVC) were mainly optimized for human perception, creating a mismatch for applications like autonomous driving or industrial surveillance.

MPEG's Video Coding for Machines (VCM) and Feature Coding for Machines (FCM) standards address this by compressing visual signals for machine analysis. In "split computing," the inference of a large neural network is split between two devices; intermediate feature tensors are reduced and compressed before being transmitted. This approach allows for interoperable bitstreams that preserve the performance of machine vision tasks (like object detection and tracking) while drastically reducing the bitrate.

### Satisfied Machine Ratio (SMR) and Task-Aware Metrics

A novel concept proposed for VCM is the Satisfied Machine Ratio (SMR), modeled after the human Satisfied User Ratio (SUR). SMR is defined as the proportion of machines that achieve a higher satisfaction score on a compressed image than a reasonable threshold. Research has shown that different machines have distinct perceptions of images at the same compression quality, and optimizing for one machine can decrease the performance of another. SMR models the general machine vision system behaviors, highlighting that machine perception exhibits unique Just Noticeable Difference (JND) characteristics that diverge from human patterns.

| Encoding Context | Optimization Target | Critical Metric | Data Domain |
|-----------------|-------------------|----------------|------------|
| Traditional Codecs | Human Vision (HVS) | PSNR / SSIM | Pixel Domain |
| MPEG-VCM | Mixed Vision | Task Accuracy (mAP) | RoI / Pixel Domain |
| MPEG-FCM | Machine Vision | SMR | Latent Feature Tensors |

---

## IX. Implementation Workout: Quantization Logic

The following Python code demonstrates the core logic of a VQ-VAE quantization layer, implementing the nearest-neighbor lookup and commitment loss mentioned in the SRD regime.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class VectorQuantizer(nn.Module):
    def __init__(self, num_embeddings, embedding_dim, commitment_cost):
        super(VectorQuantizer, self).__init__()
        self._embedding_dim = embedding_dim
        self._num_embeddings = num_embeddings
        self._embedding = nn.Embedding(self._num_embeddings, self._embedding_dim)
        self._embedding.weight.data.uniform_(-1/self._num_embeddings, 1/self._num_embeddings)
        self._commitment_cost = commitment_cost

    def forward(self, inputs):
        # Convert BCHW to BHWC
        inputs = inputs.permute(0, 2, 3, 1).contiguous()
        input_shape = inputs.shape
        flat_input = inputs.view(-1, self._embedding_dim)
        
        # Distance Workout: (a-b)^2 = a^2 + b^2 - 2ab
        distances = (torch.sum(flat_input**2, dim=1, keepdim=True) 
                    + torch.sum(self._embedding.weight**2, dim=1)
                    - 2 * torch.matmul(flat_input, self._embedding.weight.t()))
            
        # Encoding: Nearest neighbor lookup
        encoding_indices = torch.argmin(distances, dim=1).unsqueeze(1)
        encodings = torch.zeros(encoding_indices.shape[0], self._num_embeddings, device=inputs.device)
        encodings.scatter_(1, encoding_indices, 1)
        
        # Quantize: Map indices back to codebook vectors
        quantized = torch.matmul(encodings, self._embedding.weight).view(input_shape)
        
        # Loss: Semantic commitment loss
        # Encourages encoder output to commit to an embedding
        e_latent_loss = F.mse_loss(quantized.detach(), inputs)
        q_latent_loss = F.mse_loss(quantized, inputs.detach())
        loss = q_latent_loss + self._commitment_cost * e_latent_loss
        
        # Straight-through estimator
        quantized = inputs + (quantized - inputs).detach()
        
        return loss, quantized.permute(0, 3, 1, 2).contiguous()
```

---

## X. Falsifiable Predictions (2025–2035)

The trajectory we have outlined leads to several concrete, falsifiable predictions:

1. **Motion Vectors will Disappear**: Replaced by latent state updates and prediction-error residuals
2. **Bitstreams will become Latent Programs**: Decoders will execute learned generative processes seeded by symbolic tokens
3. **Pixel-Fidelity Metrics will be Abandoned**: Standards will optimize for Satisfied Machine Ratio (SMR) or task accuracy
4. **Decoder Size will Dominate**: Compression ratios will increase while decoder parameter counts grow by orders of magnitude
5. **Closed-Loop Personalization**: Personalization based on gaze will yield measurable bitrate savings at constant quality

---

## XI. Synthesis: The Future of Semantic Information Theory

The journey from scalar to structured quantization reflects a broader trajectory: a movement from the mechanical toward the biological. By embracing the complexity of Riemannian manifolds, the nuances of the human and machine visual systems, and the efficiency of neural latents, we are developing a new information theory that is capable of representing the world not just as a series of numbers, but as a rich, structured experience.

The integration of saliency-driven feedback, memory-aware temporal modeling, and perceptual primitives ensures that our data transmission systems will continue to evolve. We are moving toward a state of "ontological friction" minimization, where the forces opposing the flow of information are mitigated by the re-ontologization of the infosphere through digital ICTs. In this future, information is not merely transmitted; it is created and reconstructed through a synergistic interaction between the encoder, the medium, and the observer's mind.

Ultimately, the era of quantizing pixels is ending; the era of quantizing perception has begun. By treating information not just as a statistical property of a source but as a structural and functional property of an object and its observer, we can achieve levels of fidelity and efficiency that were once thought to be the exclusive domain of the human brain. The convergence of algorithmic information theory, differential geometry, and neurobiology provides the blueprint for this transition, where "bits follow meaning" and every pulse of data serves a specific, perceived purpose.

### Summary of Modern Compression Benchmarks

| Framework | Mechanism | Typical Gain / Efficiency | Primary Constraint |
|-----------|-----------|---------------------------|-------------------|
| Lloyd-Max SQ | Iterative Centroid Optimization | Baseline | Treats pixels as independent |
| Daala PVQ | Gain-Shape / Householder | 13.7% - 24.8% Bitrate Reduction | Harder to visualize/implement |
| Tri-Axis Lattice | Hexagonal Coordinate System | 0.4% - 24.5% over SQ | O(N²) Complexity |
| RSAVQ (LLM) | FIM Riemannian Guidance | 1.5% Accuracy improvement | Requires natural gradient compute |
| MASTC-VC | Spatial-Temporal-Channel Context | 23.93% BD-rate savings | Non-linear complexity |
| MPEG-VCM | Machine-Oriented RoI Encoding | Up to 87% Efficiency vs VVC | Machine-specific bias |

As data transmission continues to evolve, the focus will increasingly shift toward the "time-domain" and the semantic utility of information. The transition from signal-space error minimization to perceptual-space fidelity is not merely an engineering improvement; it is a fundamental shift in how we define information itself. By quantizing the manifold of human and machine experience, we are building the infrastructure for a more efficient, more intelligent, and more human-centric digital future.

---

## Philosophical Coda: Consciousness as Compression

If we follow this line of reasoning to its natural conclusion, we arrive at a profound philosophical insight: consciousness itself may be understood as a form of compression. The human mind does not store raw sensory data; it extracts patterns, builds models, and constructs narratives. Memory is not a tape recorder but a generative process that reconstructs past experiences from sparse semantic cues.

In this light, the development of semantic codecs is not merely a technical achievement but a step toward understanding and perhaps replicating the fundamental mechanisms of conscious experience. When we build systems that compress by understanding rather than by copying, we are, in a very real sense, teaching machines to perceive—to extract meaning from the chaos of sensory input.

The perceptual manifold is not just a mathematical abstraction; it is the geometric structure of conscious experience itself. Each point on this manifold represents not a signal but a state of awareness, a particular configuration of meaning and significance. To navigate this space efficiently—to transmit information across it with minimal loss—is to participate in the same process that allows minds to communicate, to share thoughts, to build culture.

As compression converges with inference, as transmission becomes coordination, we are witnessing the emergence of a new kind of information technology: one that operates not on bits but on meaning, not on signals but on understanding. This is the promise and the challenge of the perceptual manifold paradigm—to build systems that see as we see, that understand as we understand, and that, in doing so, help us see ourselves more clearly.

---

## Works Cited

1. Kolmogorov's Contributions to Information Theory and Algorithmic Complexity. https://isl.stanford.edu/~cover/papers/paper090.pdf
2. Entropy | Special Issue: Shannon Information and Kolmogorov Complexity. https://www.mdpi.com/journal/entropy/special_issues/Shannon_Kolmogorov_Complexity
3. The Hidden Order of Information: Unlocking the Secrets of Kolmogorov Complexity. https://medium.com/@timplay89/the-hidden-order-of-information-unlocking-the-secrets-of-kolmogorov-complexity-663403e1d9a3
4. RSAVQ: Riemannian Sensitivity-Aware Vector Quantization for Large Language Models. https://arxiv.org/html/2510.01240v1
5. A Survey of Geometric Optimization for Deep Learning: From Euclidean Space to Riemannian Manifold. https://www.researchgate.net/publication/387431031_A_Survey_of_Geometric_Optimization_for_Deep_Learning_From_Euclidean_Space_to_Riemannian_Manifold
6. Kolmogorov Complexity and Information Theory. https://www.cs.montana.edu/courses/fall2003/current/510/k.pdf
7. Approximations of algorithmic and structural complexity validate cognitive-behavioral experimental results. https://pmc.ncbi.nlm.nih.gov/articles/PMC9904762/
8. Multiple-Description Lattice Vector Quantization. https://homepage.tudelft.nl/c7c8y/theses/PhDThesisOstergaard.pdf
9. DB-LLM: Accurate Dual-Binarization for Efficient LLMs. https://www.researchgate.net/publication/384213471_DB-LLM_Accurate_Dual-Binarization_for_Efficient_LLMs
10. arXiv daily: Image and Video Processing (eess.IV). https://sciencecast.org/podcasts/arxiv_daily/image-and-video-processing
11. Perceptual Vector Quantization. https://jmvalin.ca/daala/pvq_demo/
12. Perceptual Vector Quantization for Video Coding. https://jmvalin.ca/papers/spie_pvq.pdf
13. ACM SIGMM Records. https://records.sigmm.org/category/issue-2023/records2301/
14. Perceptual Vector Quantization For Video Coding. https://arxiv.org/abs/1602.05209
15. Task-oriented communication for edge intelligence enabled connected robotics systems. https://theses.gla.ac.uk/85353/1/2025DiaoPhD.pdf
16. Householder Reflections. http://www.mapleprimes.com/maplesoftblog/205330-Householder-Reflections
17. GIC-DLC: Differentiable Logic Circuits for Hardware-Friendly Grayscale Image Compression. https://arxiv.org/html/2601.14130v1
18. Video coding for machines using region-of-interest-based retargeting. https://www.researchgate.net/publication/396870259_Video_coding_for_machines_using_region-of-interest-based_retargeting
19. An Open Dataset for Video Coding for Machines Standardization. https://www.researchgate.net/publication/365122065_An_Open_Dataset_for_Video_Coding_for_Machines_Standardization
20. NeurIPS 2025 Papers. https://neurips.cc/virtual/2025/papers.html
21. Time-domain brain: temporal mechanisms for brain functions. https://pmc.ncbi.nlm.nih.gov/articles/PMC11877394/
22. Perceptual Video Coding for Machines via Satisfied Machine Ratio Modeling. https://arxiv.org/html/2211.06797v3
23. An extensible framework for the deployment and management of computer vision workloads on edge platforms. https://researchrepository.ul.ie/bitstreams/3a7d87ea-a55c-40c1-aced-dba621cce0ef/download
24. Non-uniform Quantizers, Lloyd–Max Optimality and High-Rate. http://web.stanford.edu/class/ee269/Lecture_nonuniform_quantization.pdf
25. Information Support of Educationalists as an Important Function of a Postgraduate Education System. https://www.researchgate.net/publication/336159396_Information_Support_of_Educationalists_as_an_Important_Function_of_a_Postgraduate_Education_System
