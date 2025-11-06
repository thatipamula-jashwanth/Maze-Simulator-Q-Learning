from flask import Blueprint, request, jsonify
from logic.qlearning_engine import QLearningAgent
from logic.path_finder import PathFinder
import numpy as np
import os

qlearning_bp = Blueprint("qlearning", __name__)

@qlearning_bp.route("/train", methods=["POST"])
def train_qlearning():
    try:
        data = request.get_json(force=True) or {}

        grid_size = tuple(data.get("grid_size", (4, 4)))
        learning_rate = float(data.get("learning_rate", 0.1))
        discount_factor = float(data.get("discount_factor", 0.9))
        epsilon = float(data.get("epsilon", 0.1))
        episodes = int(data.get("episodes", 500))

        agent = QLearningAgent(
            grid_size=grid_size,
            learning_rate=learning_rate,
            discount_factor=discount_factor,
            epsilon=epsilon,
            episodes=episodes
        )

        result = agent.train()

        # Save Q-table as .npy
        os.makedirs("data", exist_ok=True)
        np.save("data/qtable.npy", result["q_table"])

        # Ensure q_table is a list
        q_table_safe = result["q_table"].tolist() if isinstance(result["q_table"], np.ndarray) else result["q_table"]

        return jsonify({
            "status": "success",
            "message": "Q-Learning training completed successfully.",
            "params": {
                "grid_size": grid_size,
                "learning_rate": learning_rate,
                "discount_factor": discount_factor,
                "epsilon": epsilon,
                "episodes": episodes
            },
            "results": {
                "average_reward": result["average_reward"],
                "rewards": result["rewards"],
                "q_table": q_table_safe
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@qlearning_bp.route("/path", methods=["GET"])
def get_optimal_path():
    try:
        finder = PathFinder()
        path = finder.find_path(q_table_path="data/qtable.npy")
        return jsonify({"status": "success", "path": path}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
