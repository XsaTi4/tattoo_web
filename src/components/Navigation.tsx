'use client';

import { useLanguage } from '@/context/LanguageContext';
import styles from './Navigation.module.css';

export default function Navigation() {
    const { t } = useLanguage();

    const scrollTo = (id: string) => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <nav className={styles.navBar}>
            <button onClick={() => scrollTo('about')} className={styles.navLink}>{t.nav.about}</button>
            <button onClick={() => scrollTo('studio')} className={styles.navLink}>{t.nav.studio}</button>
            <button onClick={() => scrollTo('work')} className={styles.navLink}>{t.nav.work}</button>
            <button onClick={() => scrollTo('contact')} className={styles.navLink}>{t.nav.contact}</button>
        </nav>
    );
}
