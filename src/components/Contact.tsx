'use client';

import { useLanguage } from '@/context/LanguageContext';
import styles from './Contact.module.css';
import { Mail, Phone, Instagram } from 'lucide-react';

export default function Contact() {
    const { t } = useLanguage();

    return (
        <section className={styles.contact} id="contact">
            <h2 className={styles.title}>{t.contact.title}</h2>

            <div className={styles.card}>
                <div className={styles.item}>
                    <Mail className={styles.icon} />
                    <span className={styles.label}>{t.contact.email}</span>
                    <a href="mailto:contact@nnnwwb.com" className={styles.link}>contact@nnnwwb.com</a>
                </div>

                <div className={styles.item}>
                    <Phone className={styles.icon} />
                    <span className={styles.label}>{t.contact.phone}</span>
                    <a href="tel:+37120000000" className={styles.link}>+371 20000000</a>
                </div>

                <div className={styles.item}>
                    <Instagram className={styles.icon} />
                    <span className={styles.label}>{t.contact.instagram}</span>
                    <a href="https://instagram.com/nnnwwb" target="_blank" rel="noopener noreferrer" className={styles.link}>@nnnwwb</a>
                </div>
            </div>

            <footer className={styles.footer}>
                &copy; {new Date().getFullYear()} NNNWWB. All Rights Reserved.
            </footer>
        </section>
    );
}
