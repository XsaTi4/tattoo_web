'use client';

import { useLanguage } from '@/context/LanguageContext';
import styles from './Contact.module.css';
import { Mail, Send, Instagram } from 'lucide-react';

export default function Contact() {
    const { t } = useLanguage();

    return (
        <section className={styles.contact} id="contact">
            <h2 className={styles.title}>{t.contact.title}</h2>

            <div className={styles.card}>
                <a href="mailto:valerijaavdina@inbox.lv" className={styles.gothicLink}>
                    <div className={styles.iconBox}><Mail /></div>
                    <span className={styles.linkText}>valerijaavdina@inbox.lv</span>
                </a>

                <a href="https://t.me/nnnwwb" target="_blank" rel="noopener noreferrer" className={styles.gothicLink}>
                    <div className={styles.iconBox}><Send /></div>
                    <span className={styles.linkText}>@nnnwwb</span>
                </a>

                <a href="https://instagram.com/nnnwwb" target="_blank" rel="noopener noreferrer" className={styles.gothicLink}>
                    <div className={styles.iconBox}><Instagram /></div>
                    <span className={styles.linkText}>@nnnwwb</span>
                </a>
            </div>

            <footer className={styles.footer}>
                &copy; {new Date().getFullYear()} Ink Dynasty.
            </footer>
        </section>
    );
}
