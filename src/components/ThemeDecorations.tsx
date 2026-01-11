'use client';

import config from '@/data/config.json';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import styles from './ThemeDecorations.module.css';

interface ThemeConfig {
    scroll: string[];
}

const THEMES: Record<string, ThemeConfig> = {
    halloween: {
        scroll: ['🦇', '🕸️', '👻', '🎃', '🕯️'],
    },
    newyear: {
        scroll: ['❄️', '✨', '🎁', '🎄', '☃️'],
    },
    default: {
        scroll: [],
    }
};

export default function ThemeDecorations() {
    const [theme, setTheme] = useState('default');
    const [data, setData] = useState<ThemeConfig>(THEMES.default);
    const [currentConfig, setCurrentConfig] = useState(config);

    useEffect(() => {
        setCurrentConfig(config);
        setTheme(config.theme);
        setData(THEMES[config.theme] || THEMES.default);
    }, [config]);

    if (theme === 'default') return null;

    return (
        <div className={styles.container}>
            {/* Scrolling/Floating Items */}
            {data.scroll.map((icon, index) => (
                <ScrollItem key={index} icon={icon} index={index} />
            ))}
            {/* Duplicates for density */}
            {data.scroll.map((icon, index) => (
                <ScrollItem key={`d-${index}`} icon={icon} index={index + 5} />
            ))}
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
