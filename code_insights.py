"""
CODE INSIGHTS: HOW ACTIVITY RECOGNITION WORKS
==============================================
This section shows the most important code snippets that make
the activity recognition system work for YOUR custom activities.
"""

import streamlit as st


class CodeInsightsSection:
    """
    Educational section showing critical code snippets from the activity recognition app.
    Each snippet explains key concepts in movement analytics.
    """

    def __init__(self, activity_names=None):
        self.snippets = self._create_snippets()
        # Use custom activity names or default to generic "activities"
        self.activity_context = activity_names if activity_names else ["your activities"]

    def _create_snippets(self):
        """Create all code snippets with explanations."""
        return {
            'feature_extraction': [
                {
                    'title': "📊 Detecting Movement Patterns from Acceleration",
                    'code': '''def extract_activity_features(acceleration_data, sampling_rate=100):
    # Find peaks in acceleration = movement cycles
    peaks, _ = find_peaks(acceleration_data,
                         height=1.0,      # Minimum peak height
                         distance=sampling_rate/3)  # Max 3 peaks/sec

    # Calculate movement frequency
    if len(peaks) >= 2:
        total_time = len(acceleration_data) / sampling_rate
        movement_rate = len(peaks) / total_time  # Movements per second
    else:
        movement_rate = 0

    # Calculate movement intensity
    movement_power = np.sqrt(np.mean(acceleration_data ** 2))  # RMS

    return {
        'movement_rate': movement_rate,
        'movement_power': movement_power,
        'peak_count': len(peaks)
    }''',
                    'explanation': {
                        'what': "Detects movement cycles by finding acceleration peaks",
                        'activity': "How many movement cycles per second (frequency)",
                        'importance': "Movement rate distinguishes slow vs fast activities"
                    },
                    'output_example': "Movement rate: 1.8 Hz, Power: 2.3 m/s²"
                },
                {
                    'title': "⚡ Measuring Activity Intensity (RMS & Variability)",
                    'code': '''def calculate_activity_intensity(acceleration_data):
    # Root Mean Square - measures overall movement energy
    rms_value = np.sqrt(np.mean(acceleration_data ** 2))

    # Peak-to-Peak - measures movement range
    p2p_value = np.max(acceleration_data) - np.min(acceleration_data)

    # Standard Deviation - measures movement variability
    std_value = np.std(acceleration_data)

    # Movement smoothness (coefficient of variation)
    cv_value = std_value / np.mean(acceleration_data) if np.mean(acceleration_data) != 0 else 0

    return {
        'rms': rms_value,      # Overall energy
        'p2p': p2p_value,      # Movement range
        'std': std_value,      # Variability
        'cv': cv_value         # Smoothness (lower = smoother)
    }''',
                    'explanation': {
                        'what': "Calculates different measures of movement intensity",
                        'activity': "High-intensity activities have higher RMS values",
                        'importance': "Different activities have distinct intensity profiles"
                    },
                    'output_example': "High-intensity: RMS=2.5, Low-intensity: RMS=0.8"
                },
                {
                    'title': "📈 Analyzing Movement Quality (Shape Features)",
                    'code': '''def analyze_movement_quality(acceleration_data):
    from scipy.stats import kurtosis, skew

    # Kurtosis - how peaked/flat the movement distribution is
    # High kurtosis = sharp, jerky movements
    # Low kurtosis = smooth, flowing movements
    movement_kurtosis = kurtosis(acceleration_data)

    # Skewness - asymmetry of movement pattern
    # Positive skew = right-leaning movement patterns
    # Negative skew = left-leaning movement patterns
    movement_skewness = skew(acceleration_data)

    # IQR - spread of middle 50% of movements (robust to outliers)
    q1 = np.percentile(acceleration_data, 25)
    q3 = np.percentile(acceleration_data, 75)
    movement_iqr = q3 - q1

    return {
        'kurtosis': movement_kurtosis,   # Movement sharpness
        'skewness': movement_skewness,   # Movement asymmetry
        'iqr': movement_iqr              # Movement consistency
    }''',
                    'explanation': {
                        'what': "Analyzes the statistical shape of movement patterns",
                        'activity': "Jerky movements = high kurtosis, Smooth = low kurtosis",
                        'importance': "Shape features capture movement quality, not just quantity"
                    },
                    'output_example': "Jerky activity: kurtosis=5.2, Smooth: kurtosis=0.8"
                }
            ],
            'knn_algorithm': [
                {
                    'title': "🎯 KNN Feature Selection for Activity Recognition",
                    'code': '''# KNN uses only MOTION features (4 total) for YOUR activities
motion_features = [
    "mean_magnitude",    # Average movement intensity
    "rms_magnitude",     # Root mean square (energy)
    "std_magnitude",     # Movement variability
    "p2p_magnitude"      # Movement range
]

# Select only these 4 features for KNN
X_knn = features_df[motion_features].copy()

# Why not use shape features in KNN?
# Shape features (kurtosis, skewness, etc.) have different scales
# KNN's distance calculations get confused by mixed scales

# Example for walking vs running:
# Walking: mean=1.2, rms=1.5, std=0.3, p2p=2.8
# Running: mean=2.5, rms=3.1, std=0.8, p2p=5.2''',
                    'explanation': {
                        'what': "KNN works best with simple, scaled motion features",
                        'activity': "Compares 'how much' movement, not movement patterns",
                        'importance': "Too many features confuse KNN's nearest neighbor search"
                    },
                    'output_example': "Uses 4 motion features: mean, RMS, std, peak-to-peak"
                },
                {
                    'title': "⚖️ Why Feature Scaling is CRITICAL for KNN",
                    'code': '''# WITHOUT SCALING - Features have different units!
features_before_scaling = {
    "mean_magnitude": 1.52,    # m/s²
    "rms_magnitude": 1.87,     # m/s²
    "peak_count": 3,           # count
    "kurtosis_magnitude": 0.5  # unitless
}

# KNN distance = √[(1.52-1.87)² + (3-0.5)²]
# → Peak count dominates because it's larger!

# WITH SCALING - All features comparable
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Now all features have mean=0, std=1
# KNN can compare them fairly!

# Result: KNN accuracy improves 20-40%''',
                    'explanation': {
                        'what': "Normalizes all features to same scale (mean=0, std=1)",
                        'activity': "Makes movement frequency comparable to acceleration intensity",
                        'importance': "Without scaling, KNN accuracy drops significantly"
                    },
                    'output_example': "Before scaling: 70% accuracy, After scaling: 90% accuracy"
                },
                {
                    'title': "🔍 Finding Optimal k for Your Activities",
                    'code': '''def find_optimal_k_for_activities(X_train, y_train, cv_folds=5):
    from sklearn.model_selection import cross_val_score
    from sklearn.neighbors import KNeighborsClassifier

    k_values = range(1, 16, 2)  # Test odd k values: 1, 3, 5, ..., 15
    cv_scores = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_train, y_train, cv=cv_folds)
        cv_scores.append(np.mean(scores))

    # Find k with highest CV accuracy
    optimal_k = k_values[np.argmax(cv_scores)]

    return optimal_k, cv_scores

# Example results for your custom activities:
# k=1: 85% (overfits noise)
# k=3: 89%
# k=5: 92%  ← OPTIMAL
# k=7: 91%
# k=9: 90%
# k=11: 89% (underfits patterns)''',
                    'explanation': {
                        'what': "Uses cross-validation to find the best number of neighbors",
                        'activity': "Small k overfits noise, large k misses patterns",
                        'importance': "Optimal k balances noise sensitivity and pattern recognition"
                    },
                    'output_example': "Optimal k found: 5 (tested k=1,3,5,7,9,11,13,15)"
                }
            ],
            'random_forest': [
                {
                    'title': "🌳 Random Forest Uses All Features for Deeper Insights",
                    'code': '''# Random Forest uses ALL 9 features for YOUR activities
all_features = [
    # Motion Features (4) - What you're doing
    "mean_magnitude", "rms_magnitude", "std_magnitude", "p2p_magnitude",

    # Shape Features (5) - How you're doing it
    "kurtosis_magnitude",   # Movement sharpness
    "skewness_magnitude",   # Movement asymmetry
    "median_magnitude",     # Typical movement value
    "iqr_magnitude",        # Movement consistency
    "peak_count"           # Movement cycles count
]

# RF can handle different scales naturally
X_rf = features_df[all_features].copy()

# Each tree uses random subsets of features
# This reduces overfitting and reveals feature importance

# For your custom activities, RF learns:
# 1. Motion features: How intense is the activity?
# 2. Shape features: How is the activity performed?
# 3. Combined: Complete movement signature''',
                    'explanation': {
                        'what': "RF works with complete movement profile",
                        'activity': "Analyzes both movement intensity AND movement quality",
                        'importance': "Captures complex activity patterns that simple features miss"
                    },
                    'output_example': "Uses all 9 features: 4 motion + 5 shape features"
                },
                {
                    'title': "🏆 RF Feature Importance: What Really Matters for Your Activities",
                    'code': '''# After training Random Forest on YOUR data
rf_model.fit(X_train, y_train)

# Get feature importance scores
feature_importance = rf_model.feature_importances_

# Create dictionary for interpretation
importance_dict = dict(zip(feature_names, feature_importance))

# Sort by importance
sorted_importance = sorted(importance_dict.items(),
                          key=lambda x: x[1],
                          reverse=True)

# Example results for custom activities:
# [
#     ("rms_magnitude", 0.32),     # Most important - overall energy
#     ("peak_count", 0.25),        # Movement frequency
#     ("p2p_magnitude", 0.18),     # Movement range
#     ("kurtosis_magnitude", 0.12), # Movement sharpness
#     ("std_magnitude", 0.08),     # Movement variability
#     ... other features
# ]

# Interpretation for YOUR activities:
# 1. Focus on "rms_magnitude" - it's the strongest predictor
# 2. "peak_count" matters for rhythmic activities
# 3. "kurtosis" distinguishes jerky vs smooth movements''',
                    'explanation': {
                        'what': "Shows which features most influence classification",
                        'activity': "Tells you what distinguishes your custom activities",
                        'importance': "Transforms black-box model into actionable insights"
                    },
                    'output_example': "Top features: RMS (32%), Peak count (25%), P2P (18%)"
                },
                {
                    'title': "⚡ Random Forest Hyperparameter Optimization",
                    'code': '''def optimize_random_forest_for_activities(X_train, y_train):
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import RandomForestClassifier

    param_grid = {
        'n_estimators': [50, 100, 200],      # Number of trees
        'max_depth': [None, 10, 20, 30],     # Tree depth
        'min_samples_split': [2, 5, 10],     # Minimum samples to split
        'min_samples_leaf': [1, 2, 4]        # Minimum samples per leaf
    }

    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(rf, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    return grid_search.best_params_, grid_search.best_score_

# Example optimization for your activities:
# Best parameters found:
# - n_estimators: 200 trees
# - max_depth: None (unlimited)
# - min_samples_split: 2
# - min_samples_leaf: 1
#
# Accuracy improvement: 87% → 94% (+7%)''',
                    'explanation': {
                        'what': "Systematically tests parameter combinations",
                        'activity': "Finds optimal tree depth, number of trees, etc. for YOUR data",
                        'importance': "Can improve accuracy 5-15% over default parameters"
                    },
                    'output_example': "Best params: 200 trees, unlimited depth, accuracy: 94%"
                }
            ],
            'comparison': [
                {
                    'title': "🤔 KNN vs Random Forest: Which to Choose for Your Activities?",
                    'code': '''# SIDE-BY-SIDE COMPARISON FOR YOUR ACTIVITY RECOGNITION
# ==================== KNN ===================  ============== RF ================
# Features:     4 motion features              # 9 features (motion + shape)
# Scaling:     REQUIRED                        # Not required
# Training:    Instant (stores data)           # Slow (builds trees)
# Prediction:  Slow (searches all data)        # Fast (tree traversal)
# Output:      "Similar to example X"          # "Feature Y is important"
# Best for:    Quick prototypes                # Production systems
# Accuracy:    85-90%                          # 90-95%
# Interpret:   Simple comparison               # Feature importance
# Speed:       Fast training, slow prediction  # Slow training, fast prediction

# DECISION GUIDE FOR YOUR CUSTOM ACTIVITIES:
def choose_algorithm_for_activities(requirements):
    if requirements["speed"] == "fast" and requirements["data"] == "small":
        return "KNN"  # Quick results with small data

    elif requirements["accuracy"] == "high" and requirements["interpret"] == "yes":
        return "Random Forest"  # Best accuracy + feature insights

    elif requirements["real_time"] == "yes":
        if requirements["battery"] == "critical":
            return "KNN"  # Lighter prediction
        else:
            return "Random Forest"  # Better accuracy

    else:
        return "Random Forest"  # Default for most cases''',
                    'explanation': {
                        'what': "Different algorithms for different use cases",
                        'activity': "KNN: Quick testing, RF: Final deployment",
                        'importance': "Choose based on your needs: speed vs accuracy vs interpretability"
                    },
                    'output_example': "KNN: 87% accuracy in 0.1s, RF: 92% accuracy in 2s"
                },
                {
                    'title': "🎯 When to Use Each Algorithm for Your Application",
                    'code': '''# PRACTICAL DECISION TREE FOR ACTIVITY RECOGNITION

# Scenario 1: Real-time mobile app for activity tracking
requirements_mobile = {
    "speed": "medium",
    "accuracy": "high",
    "interpret": "yes",      # Show user "improve your movement"
    "real_time": "yes",
    "battery": "moderate",
    "data": "medium"
}
# Choice: Random Forest (good accuracy, feature insights)

# Scenario 2: Quick prototype for new activity types
requirements_prototype = {
    "speed": "fast",
    "accuracy": "medium",
    "interpret": "no",       # Just need to see if it works
    "real_time": "no",
    "battery": "not_important",
    "data": "small"
}
# Choice: KNN (fast setup, works with small data)

# Scenario 3: Wearable device with limited battery
requirements_wearable = {
    "speed": "fast",
    "accuracy": "medium",
    "interpret": "no",
    "real_time": "yes",
    "battery": "critical",
    "data": "small"
}
# Choice: KNN (lightweight prediction)

# Your custom activities might need different approaches:
# - Simple activities (2-3 types): KNN often works well
# - Complex activities (5+ types): Random Forest better
# - Mixed activity types: Test both!''',
                    'explanation': {
                        'what': "Guidelines for selecting the right algorithm",
                        'activity': "Mobile apps: RF for accuracy, Wearables: KNN for battery",
                        'importance': "The right tool depends on your specific application"
                    },
                    'output_example': "Smart fitness tracker: Random Forest (accuracy > battery)"
                }
            ],
            'practical_applications': [
                {
                    'title': "🏃‍♂️ Real-World Application: Building Your Own Activity Classifier",
                    'code': '''# Simplified implementation for your custom activities
class CustomActivityClassifier:
    def __init__(self, model_type="knn"):
        if model_type == "knn":
            self.model = KNeighborsClassifier(n_neighbors=5)
            self.scaler = StandardScaler()
        else:
            self.model = RandomForestClassifier(n_estimators=100)
            self.scaler = None

    def predict_activity(self, acceleration_window, sampling_rate=100):
        # Extract features from 2-second window
        features = self.extract_features(acceleration_window, sampling_rate)

        # Scale if using KNN
        if self.scaler:
            features = self.scaler.transform([features])

        # Predict activity
        prediction = self.model.predict(features)[0]

        # Confidence score
        if hasattr(self.model, "predict_proba"):
            confidence = np.max(self.model.predict_proba(features)[0])
        else:
            confidence = 1.0

        return prediction, confidence

    def extract_features(self, data, sampling_rate):
        # Simple features for efficiency
        return [
            np.mean(data),                     # Mean intensity
            np.std(data),                      # Variability
            np.max(data) - np.min(data),       # Movement range
            len(find_peaks(data)[0]),          # Movement cycles
            kurtosis(data),                    # Movement sharpness
            skew(data)                         # Movement asymmetry
        ]

# Usage for YOUR activities:
classifier = CustomActivityClassifier(model_type="random_forest")
activity, confidence = classifier.predict_activity(acceleration_data)
# Output: ("your_activity_1", 0.92)''',
                    'explanation': {
                        'what': "Lightweight classifier for deployment",
                        'activity': "Can run on mobile devices or wearables",
                        'importance': "Shows how research translates to real products"
                    },
                    'output_example': "Prediction: activity_1, Confidence: 92%"
                },
                {
                    'title': "📱 Deploying Your Activity Recognition Model",
                    'code': '''# Steps to deploy your trained model

# 1. Save your trained model
import pickle

model_data = {
    'model': trained_model,
    'feature_names': feature_names,
    'activity_labels': activity_labels,
    'scaler': scaler if needed,
    'accuracy': test_accuracy,
    'training_date': current_date
}

with open('my_activity_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

# 2. Load and use in production
with open('my_activity_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# 3. Make predictions on new data
def predict_new_activity(new_sensor_data):
    features = extract_features(new_sensor_data)
    if 'scaler' in loaded_model:
        features = loaded_model['scaler'].transform([features])
    prediction = loaded_model['model'].predict(features)[0]
    activity_name = loaded_model['activity_labels'][prediction]
    return activity_name

# 4. For mobile deployment (TensorFlow Lite example):
import tensorflow as tf

# Convert Random Forest to mobile-friendly format
converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
tflite_model = converter.convert()

# Save for mobile app
with open('activity_model.tflite', 'wb') as f:
    f.write(tflite_model)''',
                    'explanation': {
                        'what': "How to take your model from research to production",
                        'activity': "Makes your custom activity recognition usable anywhere",
                        'importance': "The ultimate goal: turn research into real-world impact"
                    },
                    'output_example': "Model saved, ready for mobile app deployment"
                }
            ]
        }

    def display_snippet(self, category, snippet_idx):
        """Display a single code snippet with explanation."""
        snippet = self.snippets[category][snippet_idx]

        st.markdown(f"### {snippet['title']}")

        # Code display
        with st.expander("📝 View Code", expanded=True):
            st.code(snippet['code'], language='python')

        # Explanation
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**What this does:**\n{snippet['explanation']['what']}")
        with col2:
            # Use custom activity context or default
            if self.activity_context:
                context = f"How this applies to {', '.join(self.activity_context[:3])}"
                if len(self.activity_context) > 3:
                    context += f" and {len(self.activity_context) - 3} more"
            else:
                context = snippet['explanation']['activity']
            st.success(f"**Activity meaning:**\n{context}")
        with col3:
            st.warning(f"**Why it matters:**\n{snippet['explanation']['importance']}")

        # Output example
        if snippet['output_example']:
            st.markdown(f"**Example output:** `{snippet['output_example']}`")

        st.divider()

    def display_category(self, category_name, category_label):
        """Display all snippets in a category."""
        st.markdown(f"## {category_label}")

        for i in range(len(self.snippets[category_name])):
            self.display_snippet(category_name, i)

    def display_all(self):
        """Display the complete code insights section."""
        st.title(
            f"🔍 Code Insights: How {self.activity_context[0].title()} Recognition Works"
            if self.activity_context else "🔍 Code Insights: How Activity Recognition Works"
        )

        st.markdown("""
        This section shows the **most important code** that makes your custom activity
        recognition system work. Each snippet explains a key concept in movement analytics.
        """)

        # Feature Extraction
        self.display_category(
            'feature_extraction',
            "📊 Feature Extraction: From Sensors to Activity Metrics"
        )

        # KNN Algorithm
        self.display_category(
            'knn_algorithm',
            "🎯 K-Nearest Neighbors: Simple but Effective"
        )

        # Random Forest
        self.display_category(
            'random_forest',
            "🌳 Random Forest: The Power of Ensemble Learning"
        )

        # Comparison
        self.display_category(
            'comparison',
            "🤔 Algorithm Comparison: Making the Right Choice"
        )

        # Practical Applications
        self.display_category(
            'practical_applications',
            "🏃‍♂️ Practical Applications: From Research to Real Products"
        )

        # Summary
        st.markdown("---")
        st.markdown(f"""
        ### 🎓 Key Takeaways for Your {'Custom Activities' if self.activity_context else 'Activities'}:

        1. **Feature Engineering is Key**: Good features make classification easy
        2. **Different Tools for Different Jobs**:
           - **KNN**: Quick prototyping, small datasets
           - **Random Forest**: Production systems, feature insights
        3. **Think About Deployment**: Mobile vs server, battery vs accuracy
        4. **Start Simple**: Mean, RMS, and peak count often work surprisingly well

        **Next Steps:**
        - Try building your own activity classifier
        - Experiment with different features
        - Consider how you'd deploy this on your target device

        Keep exploring and happy analyzing! 🚶‍♂️👣🏃‍♂️
        """)


def add_code_insights_section(activity_names=None):
    """Add the code insights section to the activity app."""
    insights = CodeInsightsSection(activity_names)
    insights.display_all()
