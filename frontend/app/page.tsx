'use client';

import { useSession, signIn, signOut } from 'next-auth/react';
import { useEffect, useState } from 'react';
import { daftarBerita } from '@/database/berita_dengan_detail';

interface Berita {
  id: string;
  judul: string;
  tanggal: string;
  isi: string;
  gambar_url: string | Blob | null;
}

export default function Home() {
  const { data: session } = useSession();
  const [berita, setBerita] = useState<Berita[]>(daftarBerita);
  const [selected, setSelected] = useState<Berita | null>(null);
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % berita.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [berita.length]);

  const handleDetail = (item: Berita) => {
    if (!session) {
      signIn('google');
    } else {
      setSelected(item);
    }
  };

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % berita.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + berita.length) % berita.length);
  };

  return (
    <main className="bg-gray-100 min-h-screen">
      {/* Header */}
      <header className="bg-white shadow mb-8">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-4xl font-bold text-gray-800">Portal Berita</h1>
          <nav className="flex space-x-4">
            <div className="flex items-center space-x-2">
              <a
                href="#"
                className="px-4 py-2  rounded bg-gray-400 text-white hover:text-gray-800"
              >
                Home
              </a>
              <a
                href="#"
                className="px-4 py-2  rounded bg-gray-400 text-white hover:text-gray-800"
              >
                Kategori
              </a>
              <a
                href="#"
                className="px-4 py-2  rounded bg-gray-400 text-white hover:text-gray-800"
              >
                Tentang
              </a>
            </div>
            {!session ? (
              <button
                onClick={() => signIn('google')}
                className="px-4 py-2 bg-blue-600 text-white rounded cursor-pointer hover:bg-blue-700"
              >
                Login
              </button>
            ) : (
              <div className="flex items-center space-x-2">
                <span className="text-gray-700">
                  Halo, {session.user?.name}
                </span>
                <button
                  onClick={() => signOut()}
                  className="px-4 py-2 bg-red-600 text-white rounded cursor-pointer  hover:bg-red-700"
                >
                  Logout
                </button>
              </div>
            )}
          </nav>
        </div>
      </header>

      {/* Carousel */}
      <section className="mb-12 relative px-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Berita Utama</h2>
        {berita.length > 0 && (
          <div className="relative rounded-lg overflow-hidden shadow-lg">
            <img
              src={berita[currentSlide].gambar_url || ''}
              alt={berita[currentSlide].judul}
              className="w-full h-96 object-cover"
            />
            <div className="absolute inset-0 bg-black opacity-50"></div>
            <div className="absolute inset-0 flex flex-col justify-end p-6">
              <h3 className="text-2xl font-bold text-white mb-2">
                {berita[currentSlide].judul}
              </h3>
              <p className="text-sm text-gray-300">
                {berita[currentSlide].tanggal}
              </p>
            </div>
            <button
              onClick={prevSlide}
              className="absolute top-1/2 left-4 transform -translate-y-1/2 bg-white text-black rounded-full p-2 shadow hover:bg-gray-200"
            >
              &#8592;
            </button>
            <button
              onClick={nextSlide}
              className="absolute top-1/2 right-4 transform -translate-y-1/2 bg-white text-black rounded-full p-2 shadow hover:bg-gray-200"
            >
              &#8594;
            </button>
          </div>
        )}
      </section>

      {/* News List */}
      <section className="px-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">
          Berita Terkini
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {berita.slice(1).map((item) => (
            <div
              key={item.id}
              className="border rounded-lg shadow-lg bg-white overflow-hidden hover:shadow-xl transition-shadow duration-300"
            >
              <img
                src={item.gambar_url || ''}
                alt={item.judul}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h3 className="text-lg font-bold text-gray-800">
                  {item.judul}
                </h3>
                <p className="text-sm text-gray-500 mb-4">{item.tanggal}</p>
                <button
                  onClick={() => handleDetail(item)}
                  className="text-blue-600 hover:underline"
                >
                  {session ? 'Lihat detail' : 'Login untuk lihat detail'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Detail Modal */}
      {selected && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-lg max-w-2xl w-full p-6 overflow-auto max-h-[90vh]">
            <h2 className="text-2xl font-bold mb-2 text-gray-800">
              {selected.judul}
            </h2>
            <p className="text-sm text-gray-600 mb-4">{selected.tanggal}</p>
            <img
              src={selected.gambar_url || ''}
              alt={selected.judul}
              className="w-full h-64 object-cover rounded mb-4"
            />
            <p className="whitespace-pre-wrap text-sm text-gray-700">
              {selected.isi}
            </p>
            <div className="mt-4 text-right">
              <button
                onClick={() => setSelected(null)}
                className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
              >
                Tutup
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12">
        <div className="container mx-auto px-6 py-8 flex flex-col md:flex-row justify-between">
          <div>
            <h2 className="text-xl font-bold">Portal Berita</h2>
            <p className="mt-2 text-gray-400">
              Menyajikan berita terkini dan terpercaya.
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <h3 className="text-lg font-semibold">Navigasi</h3>
            <ul className="mt-2 space-y-2">
              <li>
                <a href="#" className="hover:underline">
                  Beranda
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Kategori
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Tentang Kami
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Kontak
                </a>
              </li>
            </ul>
          </div>
          <div className="mt-4 md:mt-0">
            <h3 className="text-lg font-semibold">Ikuti Kami</h3>
            <ul className="mt-2 space-y-2">
              <li>
                <a href="#" className="hover:underline">
                  Facebook
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Twitter
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Instagram
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="bg-gray-700 text-center py-4">
          <p className="text-gray-400">
            &copy; 2025 Portal Berita. All rights reserved.
          </p>
        </div>
      </footer>
    </main>
  );
}
