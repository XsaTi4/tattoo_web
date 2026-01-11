'use client';

import config from '@/data/config.json';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useEffect, useState } from 'react';
import styles from './ThemeDecorations.module.css';

const THEMES = {
    halloween: {
        top: '🎃',
        scroll: ['🦇', '🕸️', '👻'],
        bottom: ['🕯️', '🕯️']
    },
    newyear: {
        top: '🎄',
        scroll: ['❄️', '✨', '🎁'],
        bottom: ['☃️', '☃️']
    },
    default: {
        top: null,
        scroll: [],
        bottom: []
    }
};

export default function ThemeDecorations() {
    const [theme, setTheme] = useState('default');
    const [data, setData] = useState(THEMES.default);
    const [currentConfig, setCurrentConfig] = useState(config);
    const { scrollYProgress } = useScroll();
    const rotate = useTransform(scrollYProgress, [0, 1], [0, 360]);

    useEffect(() => {
        setCurrentConfig(config);
        setTheme(config.theme);
        // @ts-ignore
        setData(THEMES[config.theme] || THEMES.default);
    }, [config]);

    if (theme === 'default') return null;

    return (
        <div className={styles.container}>
            {/* Fixed Top Decoration */}
            {data.top && (
                <motion.div
                    className={styles.topDeco}
                    animate={{ scale: [1, 1.1, 1], filter: ["drop-shadow(0 0 10px gold)", "drop-shadow(0 0 20px red)", "drop-shadow(0 0 10px gold)"] }}
                    transition={{ duration: 3, repeat: Infinity }}
                >
                    {data.top}
                </motion.div>
            )}

            {/* Scrolling/Floating Items */}
            {data.scroll.map((icon, index) => (
                <ScrollItem key={index} icon={icon} index={index} />
            ))}
            {/* Duplicates for density */}
            {data.scroll.map((icon, index) => (
                <ScrollItem key={`d-${index}`} icon={icon} index={index + 5} />
            ))}

            {/* Fixed Bottom Decoration */}
            <div className={styles.bottomRow}>
                {data.bottom.map((icon, index) => (
                    <motion.div
                        key={index}
                        className={styles.bottomDeco}
                        animate={{ y: [0, -10, 0] }}
                        transition={{ duration: 2, repeat: Infinity, delay: index }}
                    >
                        {icon}
                    </motion.div>
                ))}
            </div>
        </div>
    );
}

function ScrollItem({ icon, index }: { icon: string; index: number }) {
    const randomX = (index * 13 + 7) % 90; // determinstic random-ish pos
    const delay = index * 0.8;

    return (
        <motion.div
            className={styles.floatingDeco}
            style={{ left: `${randomX}vw` }}
            initial={{ y: -100, opacity: 0 }}
            animate={{
                y: '100vh',
                rotate: [0, 360],
                opacity: [0, 1, 1, 0]
            }}
            transition={{
                duration: 15 + index,
                repeat: Infinity,
                ease: "linear",
                delay: delay
            }}
        >
            {icon}
        </motion.div>
    );
}
