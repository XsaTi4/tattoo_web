'use client';

import { useState } from 'react';
import { useLanguage } from '@/context/LanguageContext';
import styles from './Gallery.module.css';
import { X, ZoomIn, ZoomOut } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import CardCarousel from './CardCarousel';

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
    const [zoomLevel, setZoomLevel] = useState(1);

    const openLightbox = (id: number) => {
        setSelectedImage(id);
        setZoomLevel(1);
    };

    const closeLightbox = () => setSelectedImage(null);

    const handleZoom = (e: React.MouseEvent) => {
        e.stopPropagation();
        setZoomLevel(prev => prev === 1 ? 2 : 1);
    };

    return (
        <section className={styles.gallery} id="work">
            <div className={styles.header}>
                <h2 className={styles.heading}>{t.works.title}</h2>
                <p className={styles.intro}>{t.works.intro}</p>
            </div>

            {/* Main Attraction: Animated Carousel */}
            <div className={styles.carouselSection}>
                <CardCarousel images={artworks} onOpenGallery={openLightbox} />
            </div>

            <div className={styles.gridBtnContainer}>
                <button className={styles.gridBtn} onClick={() => openLightbox(artworks[0].id)}>
                    {t.works.cta}
                </button>
            </div>

            <AnimatePresence>
                {selectedImage && (
                    <motion.div
                        className={styles.lightbox}
                        onClick={closeLightbox}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <div className={styles.toolbar}>
                            <button onClick={handleZoom} className={styles.toolBtn}>
                                {zoomLevel === 1 ? <ZoomIn /> : <ZoomOut />}
                            </button>
                            <button onClick={closeLightbox} className={styles.toolBtn}>
                                <X />
                            </button>
                        </div>

                        <div className={styles.lightboxContent} onClick={(e) => e.stopPropagation()}>
                            <motion.div
                                className={styles.lightboxImgContainer}
                                animate={{ scale: zoomLevel }}
                                transition={{ type: "spring", stiffness: 300, damping: 30 }}
                                style={{ cursor: zoomLevel === 1 ? 'zoom-in' : 'zoom-out' }}
                                onClick={handleZoom}
                            >
                                <img
                                    src={artworks.find(a => a.id === selectedImage)?.src}
                                    alt="Full size"
                                    className={styles.lightboxImg}
                                />
                            </motion.div>
                            {zoomLevel === 1 && (
                                <p className={styles.lightboxCaption}>{artworks.find(a => a.id === selectedImage)?.title}</p>
                            )}

                            {/* Thumbnail Strip for quick nav */}
                            {zoomLevel === 1 && (
                                <div className={styles.strip}>
                                    {artworks.map(art => (
                                        <img
                                            key={art.id}
                                            src={art.src}
                                            className={`${styles.stripImg} ${selectedImage === art.id ? styles.activeStrip : ''}`}
                                            onClick={(e) => { e.stopPropagation(); openLightbox(art.id); }}
                                        />
                                    ))}
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </section>
    );
}
