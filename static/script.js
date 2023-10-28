document.addEventListener('DOMContentLoaded', function () {
  const predictButton = document.querySelector('#predictButton');
  const resetButton = document.querySelector('#resetButton');
  const aboutButton = document.getElementById('aboutButton');
  const fraudPreventionButton = document.getElementById('fraudPreventionButton');
  const creditCardForm = document.getElementById('creditCardForm');
  const predictionResult = document.getElementById('predictionResult');

  // Tambahkan event listener ke tombol reset
  resetButton.addEventListener('click', function (e) {
    e.preventDefault();
    creditCardForm.reset();
    clearPrediction();
  });

  // Fungsi clearPrediction untuk menghapus hasil prediksi
  function clearPrediction() {
    const predictionLabel = document.getElementById('predictionLabel');
    predictionLabel.innerText = '';

    // Juga sembunyikan alasan penipuan jika ada
    const fraudReasons = document.getElementById('fraudReasons');
    if (fraudReasons) {
      fraudReasons.innerHTML = ''; // Kosongkan kontennya
      fraudReasons.style.display = 'none';
    }
  }

  // Tambahkan event listener ke tombol prediksi
  predictButton.addEventListener('click', function (e) {
    e.preventDefault();
    const formData = new FormData(creditCardForm);

    // Validasi input
    let isValid = true;
    const emptyFields = []; // Array untuk menyimpan nama bidang yang kosong

    for (const [key, input] of formData.entries()) {
      if (input === '') {
        isValid = false;
        emptyFields.push(key); // Simpan nama bidang yang kosong
      }
    }

    if (!isValid) {
      alert(`Harap isi semua bidang!!!`);
      alert(`Harap isi bidang:\n${emptyFields.join('\n')}`);
      return;
    }

    fetch('/', {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Gagal melakukan permintaan prediksi.');
        }
        return response.json();
      })
      .then((data) => {
        const predictionLabel = document.getElementById('predictionLabel');
        predictionLabel.innerText = 'Hasil Prediksi: ' + data.prediction;




      })
      .catch((error) => {
        console.error(error);
        alert('Terjadi kesalahan saat melakukan permintaan prediksi.');
      });
  });

  // Tambahkan event listener untuk tombol "Tentang Kami"
  aboutButton.addEventListener('click', function () {
    window.location.href = '/about'; // Ganti dengan URL halaman "about"
  });

  // Tambahkan event listener untuk tombol "Saran Pencegahan Penipuan"
  fraudPreventionButton.addEventListener('click', function () {
    window.location.href = '/fraud-prevention'; // Ganti dengan URL halaman "fraud-prevention"
  });
});
