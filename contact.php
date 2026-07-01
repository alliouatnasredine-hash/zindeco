<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $nom = trim($_POST["nom"] ?? "");
    $telephone = trim($_POST["telephone"] ?? "");
    $email = trim($_POST["email"] ?? "");
    $ville = trim($_POST["ville"] ?? "");
    $service = trim($_POST["service"] ?? "");
    $message = trim($_POST["message"] ?? "");

    $nom = htmlspecialchars($nom, ENT_QUOTES, "UTF-8");
    $telephone = htmlspecialchars($telephone, ENT_QUOTES, "UTF-8");
    $email = htmlspecialchars($email, ENT_QUOTES, "UTF-8");
    $ville = htmlspecialchars($ville, ENT_QUOTES, "UTF-8");
    $service = htmlspecialchars($service, ENT_QUOTES, "UTF-8");
    $message = htmlspecialchars($message, ENT_QUOTES, "UTF-8");

    if ($nom === "" || $telephone === "" || $email === "" || $message === "") {
        echo "Veuillez remplir tous les champs obligatoires.";
        exit;
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo "L'adresse e-mail est invalide.";
        exit;
    }

    $destinataire = "alliouatbzh@gmail.com";
    $sujet = "Nouvelle demande de devis - ZINDECO PEINTURE";
    $contenu = "Nouvelle demande de devis\n\n"
        . "Nom : $nom\n"
        . "Téléphone : $telephone\n"
        . "Email : $email\n"
        . "Ville : $ville\n"
        . "Prestation : $service\n\n"
        . "Message :\n$message\n";

    $headers = "From: ZINDECO PEINTURE <no-reply@zindeco-peinture-rennes.fr>\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8";

    if (@mail($destinataire, $sujet, $contenu, $headers)) {
        header("Location: merci.html");
        exit;
    }

    error_log("Échec d'envoi du formulaire de contact pour $email");
    echo "Une erreur est survenue lors de l'envoi du formulaire. Veuillez réessayer plus tard.";
}
?>