<?php
// Incluir os arquivos necessários do PHPMailer - Referenciar caminho da pasta src copiada para os seu projeto
require 'src/PHPMailer.php';
require 'src/SMTP.php';
require 'src/Exception.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

$mail = new PHPMailer(true);

try {
    // Configurações do servidor
    $mail->isSMTP();
    $mail->Host       = 'smtp.gmail.com';
    $mail->SMTPAuth   = true;
    $mail->Username   = 'seu_email@gmail.com'; //e-mail do remetente - no caso o seu e-mail
    $mail->Password   = 'senha de 16 caracteres gerada via Google'; //senha do app gerado via Google
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
    $mail->Port       = 465;

    // Configurações do remetente e destinatário
    $mail->setFrom('seu_email@gmail.com', 'descrição do remetente');
    $mail->addAddress('email_destinatario', 'descrição do destinatário');

    // Conteúdo do e-mail
    $mail->isHTML(true);
    $mail->Subject = 'Assunto do e-mail';
    $mail->Body    = 'Este é o corpo do e-mail <b>em HTML!</b>';
    $mail->AltBody = 'Este é o corpo do e-mail em texto plano para clientes de e-mail que não suportam HTML.';

    $mail->send();
    echo 'Mensagem enviada com sucesso';
} catch (Exception $e) {
    echo "A mensagem não pôde ser enviada. Mailer Error: {$mail->ErrorInfo}";
}
?>
