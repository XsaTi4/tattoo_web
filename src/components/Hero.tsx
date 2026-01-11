'use client';

import { useLanguage } from '@/context/LanguageContext';
import styles from './Hero.module.css';
import LanguageSwitcher from './LanguageSwitcher';

export default function Hero() {
    const { t } = useLanguage();

    return (
        <section className={styles.hero}>
            <div className={styles.overlay}></div>
            <nav className={styles.nav}>
                <LanguageSwitcher />
            </nav>

            <div className={styles.content}>
                <h1 className={styles.title}>{t.hero.title}</h1>
                <p className={styles.subtitle}>{t.hero.subtitle}</p>
                <button className={styles.cta} onClick={() => document.getElementById('work')?.scrollIntoView({ behavior: 'smooth' })}>
                    {t.hero.cta}
                </button>
            </div>
        </section>
    );
}
