'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/context/LanguageContext';
import styles from './Navigation.module.css';
import { motion } from 'framer-motion';

export default function Navigation() {
    const { t } = useLanguage();
    const [activeSection, setActiveSection] = useState('about');

    const scrollTo = (id: string) => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setActiveSection(entry.target.id);
                }
            });
        }, { threshold: 0.5 }); // 50% visible means active

        const sections = ['about', 'studio', 'work', 'contact'];
        sections.forEach(id => {
            const element = document.getElementById(id);
            if (element) observer.observe(element);
        });

        return () => observer.disconnect();
    }, []);

    const navItems = [
        { id: 'about', label: t.nav.about },
        { id: 'studio', label: t.nav.studio },
        { id: 'work', label: t.nav.work },
        { id: 'contact', label: t.nav.contact },
    ];

    return (
        <nav className={styles.navBar}>
            {navItems.map((item) => (
                <button
                    key={item.id}
                    onClick={() => scrollTo(item.id)}
                    className={`${styles.navLink} ${activeSection === item.id ? styles.active : ''}`}
                >
                    {activeSection === item.id && (
                        <motion.div
                            layoutId="activeTab"
                            className={styles.activeIndicator}
                            transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        />
                    )}
                    <span className={styles.linkText}>{item.label}</span>
                </button>
            ))}
        </nav>
    );
}
