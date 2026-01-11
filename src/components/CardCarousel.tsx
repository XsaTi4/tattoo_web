'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from './CardCarousel.module.css';

interface CardCarouselProps {
    images: { id: number; src: string; title: string }[];
    onOpenGallery: (id: number) => void;
}

export default function CardCarousel({ images, onOpenGallery }: CardCarouselProps) {
    const [index, setIndex] = useState(0);

    useEffect(() => {
        const timer = setInterval(() => {
            setIndex((prev) => (prev + 1) % images.length);
        }, 4000);
        return () => clearInterval(timer);
    }, [images.length]);

    return (
        <div className={styles.carouselContainer}>
            <AnimatePresence mode='popLayout'>
                {images.map((img, i) => {
                    // Calculate relative position to current index
                    const offset = (i - index + images.length) % images.length;
                    // Show only 3 cards
                    if (offset > 2 && offset < images.length - 1) return null;

                    let zIndex = 3 - offset;
                    let scale = 1 - offset * 0.1;
                    let x = offset * 40;
                    let opacity = 1 - offset * 0.2;

                    // Special case for the "entering" card (last one wrapping around)
                    if (offset === images.length - 1) {
                        zIndex = 0;
                        scale = 0.8;
                        x = -40;
                        opacity = 0;
                    }

                    return (
                        <motion.div
                            key={img.id}
                            layoutId={`card-${img.id}`}
                            className={styles.card}
                            initial={{ scale: 0.8, x: 100, opacity: 0 }}
                            animate={{
                                scale,
                                x,
                                zIndex,
                                opacity,
                                filter: offset === 0 ? 'blur(0px)' : 'blur(2px)'
                            }}
                            exit={{ opacity: 0, x: -100 }}
                            transition={{ duration: 0.8, ease: "easeInOut" }}
                            onClick={() => onOpenGallery(img.id)}
                            style={{
                                pointerEvents: offset === 0 ? 'auto' : 'none'
                            }}
                        >
                            <img src={img.src} alt={img.title} className={styles.image} />
                        </motion.div>
                    );
                })}
            </AnimatePresence>
        </div>
    );
}
