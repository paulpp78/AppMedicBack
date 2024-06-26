from Repository.SignalementRepository import SignalementRepository
from auth.auth import require_auth
from bson import ObjectId, errors as bson_errors
from db.mongodb import get_mongo_client
from flask import request, jsonify
from service.SignalementService import SignalementService


class SignalementRoutes:
    @staticmethod
    def init_app(app):
        service = SignalementService(SignalementRepository(get_mongo_client()))

        @app.route("/signalement/<signalement_id>", methods=["PUT"])
        @require_auth()
        def update_signalement(signalement_id):
            data = request.json
            pseudo, code_cip = data.get("pseudo"), data.get("code_cip")
            if not pseudo or not code_cip:
                return jsonify({"error": "Pseudo et CIP sont requis"}), 400
            try:
                modified_count = service.update_signalement(
                    ObjectId(signalement_id), pseudo, code_cip
                )
                return (
                    jsonify(
                        {
                            "message": "Signalement mis à jour",
                            "modified_count": modified_count,
                        }
                    ),
                    200,
                )
            except ValueError as ve:
                return jsonify({"error": str(ve)}), 400
            except bson_errors.InvalidId:
                return jsonify({"error": "ID de signalement invalide"}), 400

        @app.route("/signalement", methods=["POST"])
        @require_auth()
        def create_signalement():
            data = request.json
            pseudo, code_cip = data.get("pseudo"), data.get("code_cip")
            if not pseudo or not code_cip:
                return jsonify({"error": "Pseudo et CIP sont requis"}), 400
            try:
                created_count = service.create_signalement(pseudo, code_cip)
                return (
                    jsonify(
                        {
                            "message": "Signalement créé",
                            "created_count": created_count,
                        }
                    ),
                    200,
                )
            except ValueError as ve:
                return jsonify({"error": str(ve)}), 400

        @app.route("/signalement/<signalement_id>", methods=["DELETE"])
        @require_auth()
        def delete_signalement(signalement_id):
            try:
                service.delete_signalement(ObjectId(signalement_id))
                return jsonify({"message": "Signalement supprimé"}), 200
            except bson_errors.InvalidId:
                return jsonify({"error": "ID de signalement invalide"}), 400

        @app.route("/signalement/<signalement_id>", methods=["GET"])
        @require_auth()
        def get_signalement(signalement_id):
            try:
                signalement = service.get_signalement(ObjectId(signalement_id))
                if signalement:
                    signalement["_id"] = str(signalement["_id"])
                    return jsonify(signalement), 200
                else:
                    return jsonify({"error": "Signalement non trouvé"}), 404
            except bson_errors.InvalidId:
                return jsonify({"error": "ID de signalement invalide"}), 400

        @app.route("/signalement", methods=["GET"])
        # @require_auth()
        def get_signalements():
            signalements = service.get_signalements()
            signalements_list = list(signalements)
            for signalement in signalements_list:
                signalement["_id"] = str(signalement["_id"])
            return jsonify(signalements_list), 200
