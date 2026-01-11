'use client';

import { useState } from 'react';
import { useLanguage } from '@/context/LanguageContext';
import styles from './Gallery.module.css';
import Frame from './Frame';
import { X } from 'lucide-react';

// Placeholder data - replace with real images later
const artworks = [
    { id: 1, src: '/images/tattoo-1.png', title: 'Gothic Raven' },
    { id: 2, src: '/images/tattoo-1.png', title: 'Skull Study' },
    { id: 3, src: '/images/tattoo-1.png', title: 'Raven' },
    { id: 4, src: '/images/tattoo-1.png', title: 'Abstract Lines' },
    { id: 5, src: '/images/tattoo-1.png', title: 'Dark Sleeve' },
    { id: 6, src: '/images/tattoo-1.png', title: 'Geometric' },
];

export default function Gallery() {
    const { t } = useLanguage();
    const [selectedImage, setSelectedImage] = useState<number | null>(null);

    const openLightbox = (id: number) => setSelectedImage(id);
    const closeLightbox = () => setSelectedImage(null);

    return (
        <section className={styles.gallery} id="work">
            <h2 className={styles.heading}>{t.nav.work}</h2>

            <div className={styles.grid}>
                {artworks.map((art) => (
                    <div key={art.id} className={styles.item} onClick={() => openLightbox(art.id)}>
                        <Frame className={styles.frameHover}>
                            <div className={styles.imgContainer}>
                                {/* Using standard img for simplicity here, next/image would be better but requires config for local sometimes or just works */}
                                <img src={art.src} alt={art.title} className={styles.galleryImg} />
                            </div>
                        </Frame>
                    </div>
                ))}
            </div>

            {selectedImage && (
                <div className={styles.lightbox} onClick={closeLightbox}>
                    <button className={styles.closeBtn} onClick={closeLightbox}>
                        <X size={32} />
                    </button>
                    <div className={styles.lightboxContent} onClick={(e) => e.stopPropagation()}>
                        <div className={styles.lightboxImgContainer}>
                            <img
                                src={artworks.find(a => a.id === selectedImage)?.src}
                                alt="Full size"
                                className={styles.lightboxImg}
                            />
                        </div>
                        <p className={styles.lightboxCaption}>{artworks.find(a => a.id === selectedImage)?.title}</p>
                    </div>
                </div>
            )}
        </section>
    );
}
