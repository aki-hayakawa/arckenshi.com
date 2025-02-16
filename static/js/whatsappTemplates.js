let messageList = [
                    `Layari MyLatih.com untuk log masuk ke akaun anda. Sila ikuti langkah-langkah berikut:

Laman utama > Tekan "Log masuk" (butang sebelah kanan atas) > Masukkan nama pengguna dan kata laluan > Tekan butang "Log masuk" > Papan pemuka

Setelah log masuk, anda boleh mula mengikuti kursus Latihan Teknologi Pertanian Digital secara percuma. Peserta yang berjaya menamatkan kursus di platform MyLatih akan mendapat sijil yang disahkan oleh pihak MDEC.

Sekian, terima kasih.`,
                    `Layari MyLatih.com untuk kemaskini maklumat anda. Sila ikuti langkah-langkah berikut:

Log masuk di laman utama > Klik ikon bergambar "User menu" (butang sebelah kanan atas) > Klik "Profil" > Klik butang ubahsuai di profil anda dan tekan "save"

Setelah log masuk, anda boleh mula mengikuti kursus Latihan Teknologi Pertanian Digital secara percuma. Peserta yang berjaya menamatkan kursus di platform MyLatih akan mendapat sijil yang disahkan oleh pihak MDEC.

Sekian, terima kasih.`,
                ];

function insertIntoTextArea(index){
    document.getElementById('messageTextArea').innerHTML = messageList[index];
}