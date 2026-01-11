'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import styles from './StudioGallery.module.css';

interface StudioImage {
    id: number;
    src: string;
    title: string;
}

interface StudioGalleryProps {
    images: StudioImage[];
}

export default function StudioGallery({ images }: StudioGalleryProps) {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [direction, setDirection] = useState(0);

    // Auto-play
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentIndex((prev) => (prev + 1) % images.length);
            setDirection(1);
        }, 5000);
        return () => clearInterval(timer);
    }, [images.length]);

    const paginate = (newDirection: number) => {
        setDirection(newDirection);
        let newIndex = currentIndex + newDirection;
        if (newIndex < 0) newIndex = images.length - 1;
        if (newIndex >= images.length) newIndex = 0;
        setCurrentIndex(newIndex);
    };

    const nextSlide = () => paginate(1);
    const prevSlide = () => paginate(-1);

    if (!images || images.length === 0) return null;

    return (
        <div className={styles.galleryContainer}>
            <div className={styles.slider}>
                <AnimatePresence initial={false} custom={direction}>
                    <motion.img
                        key={currentIndex}
                        src={images[currentIndex].src}
                        custom={direction}
                        initial={{ opacity: 0, x: direction > 0 ? 100 : -100 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: direction > 0 ? -100 : 100 }}
                        transition={{ duration: 0.5 }}
                        className={styles.image}
                        alt={images[currentIndex].title}
                    />
                </AnimatePresence>

                <button className={`${styles.navBtn} ${styles.prev}`} onClick={prevSlide}>
                    <ChevronLeft />
                </button>
                <button className={`${styles.navBtn} ${styles.next}`} onClick={nextSlide}>
                    <ChevronRight />
                </button>

                <div className={styles.indicators}>
                    {images.map((_, idx) => (
                        <div
                            key={idx}
                            className={`${styles.dot} ${idx === currentIndex ? styles.activeDot : ''}`}
                            onClick={() => {
                                setDirection(idx > currentIndex ? 1 : -1);
                                setCurrentIndex(idx);
                            }}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
