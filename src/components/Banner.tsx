'use client';

import { useEffect, useState } from 'react';
import styles from './Banner.module.css';
import { useLanguage } from '@/context/LanguageContext';
import config from '@/data/config.json';

export default function Banner() {
    const { language } = useLanguage();
    // Using state to ensure hydration matches, but updating it via effect when config changes
    const [currentConfig, setCurrentConfig] = useState(config);

    useEffect(() => {
        // Update local state when the imported module changes (Hot Module Replacement / Fast Refresh)
        setCurrentConfig(config);

        // Set theme attribute on body
        document.body.setAttribute('data-theme', config.theme);
    }, [config]); // Depend on config to re-run if it changes

    if (!currentConfig.showBanner) return null;

    return (
        <div className={`${styles.banner} ${styles[currentConfig.theme]}`}>
            <span className={styles.text}>{currentConfig.bannerText[language] || currentConfig.bannerText.en}</span>
        </div>
    );
}
