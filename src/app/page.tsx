
import Hero from "@/components/Hero";
import About from "@/components/About";
import Gallery from "@/components/Gallery";
import Contact from "@/components/Contact";
import ScrollReveal from "@/components/ScrollReveal";

export default function Home() {
  return (
    <main>
      <Hero />
      <ScrollReveal>
        <About />
      </ScrollReveal>
      <ScrollReveal delay={200}>
        <Gallery />
      </ScrollReveal>
      <ScrollReveal delay={400}>
        <Contact />
      </ScrollReveal>
    </main>
  );
}
