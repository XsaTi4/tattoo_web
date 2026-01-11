'use client';

import { useLanguage } from '@/context/LanguageContext';
import config from '@/data/config.json';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import styles from './ThemeDecorations.module.css';

const THEME_ICONS: Record<string, string[]> = {
    halloween: ['🎃', '👻', '🦇', '🕸️'],
    newyear: ['🎄', '🎅', '❄️', '🎁', '✨'],
    default: [] // No decorations for default
};

export default function ThemeDecorations() {
    const [theme, setTheme] = useState('default');
    const [icons, setIcons] = useState<string[]>([]);
    // Use config to track updates
    const [currentConfig, setCurrentConfig] = useState(config);

    useEffect(() => {
        setCurrentConfig(config);
        setTheme(config.theme);
        setIcons(THEME_ICONS[config.theme] || []);
    }, [config]); // Re-run when config module updates (HMR)

    if (theme === 'default' || icons.length === 0) return null;

    return (
        <div className={styles.container}>
            {icons.map((icon, index) => (
                <DecorationItem key={index} icon={icon} index={index} />
            ))}
            {/* Add a few more random ones for density if needed */}
            {icons.map((icon, index) => (
                <DecorationItem key={`dup-${index}`} icon={icon} index={index + 5} />
            ))}
        </div>
    );
}

function DecorationItem({ icon, index }: { icon: string; index: number }) {
    // Randomize initial position
    const randomX = Math.floor(Math.random() * 90) + 5; // 5% to 95%
    const randomY = Math.floor(Math.random() * 80) + 10; // 10% to 90%
    const delay = index * 0.5;

    return (
        <motion.div
            className={styles.decoration}
            initial={{ x: `${randomX}vw`, y: -100, opacity: 0 }}
            animate={{
                y: [`${randomY}vh`, `${randomY + 5}vh`, `${randomY}vh`],
                rotate: [0, 10, -10, 0],
                opacity: 0.8
            }}
            transition={{
                y: { duration: 4, repeat: Infinity, ease: "easeInOut" },
                rotate: { duration: 6, repeat: Infinity, ease: "easeInOut" },
                opacity: { duration: 1 },
                delay: delay
            }}
            drag
            dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
            dragElastic={0.2}
            whileHover={{ scale: 1.2, cursor: 'grab' }}
            whileTap={{ scale: 0.9, cursor: 'grabbing' }}
        >
            {icon}
        </motion.div>
    );
}
