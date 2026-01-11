'use client';

import { useLanguage } from '@/context/LanguageContext';
import styles from './LanguageSwitcher.module.css';

export default function LanguageSwitcher() {
    const { language, setLanguage } = useLanguage();

    return (
        <div className={styles.switcher}>
            <button
                className={`${styles.btn} ${language === 'lv' ? styles.active : ''}`}
                onClick={() => setLanguage('lv')}
            >
                LV
            </button>
            <span className={styles.divider}>|</span>
            <button
                className={`${styles.btn} ${language === 'ru' ? styles.active : ''}`}
                onClick={() => setLanguage('ru')}
            >
                RU
            </button>
            <span className={styles.divider}>|</span>
            <button
                className={`${styles.btn} ${language === 'en' ? styles.active : ''}`}
                onClick={() => setLanguage('en')}
            >
                EN
            </button>
        </div>
    );
}
