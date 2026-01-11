'use client';

import { useLanguage } from '@/context/LanguageContext';
import styles from './About.module.css';
import Frame from './Frame';
import { motion } from 'framer-motion';

export default function About() {
    const { t } = useLanguage();

    return (
        <section className={styles.container} id="about">
            <div className={styles.section}>
                <div className={styles.textBlock}>
                    <h2 className={styles.heading}>{t.about.title}</h2>
                    <p className={styles.text}>{t.about.description}</p>
                    <br />
                    <p className={styles.text} style={{ fontStyle: 'italic', color: 'var(--accent)' }}>{t.about.intro}</p>
                </div>
                <motion.div
                    className={styles.imageBlock}
                    initial={{ opacity: 0, x: 50 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.8 }}
                >
                    <Frame>
                        {/* Placeholder for artist photo */}
                        <div className={styles.placeholderImg}>PHOTO</div>
                    </Frame>
                </motion.div>
            </div>

            <div className={`${styles.section} ${styles.reverse}`} id="studio">
                <div className={styles.textBlock}>
                    <h2 className={styles.heading}>{t.studio.title}</h2>
                    <p className={styles.text}>{t.studio.description}</p>
                </div>
                <motion.div
                    className={styles.imageBlock}
                    initial={{ opacity: 0, x: -50 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.8 }}
                >
                    <Frame>
                        {/* Placeholder for studio photo */}
                        <div className={styles.placeholderImg}>STUDIO</div>
                    </Frame>
                </motion.div>
            </div>
        </section>
    );
}
