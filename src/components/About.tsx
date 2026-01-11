'use client';

import { useLanguage } from '@/context/LanguageContext';
import styles from './About.module.css';
import Frame from './Frame';

export default function About() {
    const { t } = useLanguage();

    return (
        <section className={styles.container} id="about">
            <div className={styles.section}>
                <div className={styles.textBlock}>
                    <h2 className={styles.heading}>{t.about.title}</h2>
                    <p className={styles.text}>{t.about.description}</p>
                </div>
                <div className={styles.imageBlock}>
                    <Frame>
                        {/* Placeholder for artist photo */}
                        <div className={styles.placeholderImg}>PHOTO</div>
                    </Frame>
                </div>
            </div>

            <div className={`${styles.section} ${styles.reverse}`}>
                <div className={styles.textBlock}>
                    <h2 className={styles.heading}>{t.studio.title}</h2>
                    <p className={styles.text}>{t.studio.description}</p>
                </div>
                <div className={styles.imageBlock}>
                    <Frame>
                        {/* Placeholder for studio photo */}
                        <div className={styles.placeholderImg}>STUDIO</div>
                    </Frame>
                </div>
            </div>
        </section>
    );
}
