import pypdf
import re
import sys
import os
import traceback
import sys
from pypdf.generic import NameObject, StreamObject, IndirectObject, ArrayObject

# Aumento il limite di ricorsione al massimo per superare eventuali catene di riferimenti profonde
sys.setrecursionlimit(3000)

def extract_content_stream_data(content_object) -> str:
    """
    Estrae i dati del content stream, gestendo array e riferimenti in modo robusto.
    """
    
    # CASO 1: L'oggetto è un riferimento indiretto. Risolviamo e continuiamo.
    if isinstance(content_object, IndirectObject):
        try:
            # Risolve il riferimento per ottenere l'oggetto contenuto
            content_object = content_object.get_object() 
        except Exception:
            return ""
        
        # Continuiamo l'analisi con l'oggetto risolto (chiamata ricorsiva implicita)
        return extract_content_stream_data(content_object)

    # CASO 2: L'oggetto è un blocco di dati grezzi (bytes)
    if isinstance(content_object, bytes):
        return content_object.decode('latin-1')

    # CASO 3: Array di stream (più stream per pagina)
    if isinstance(content_object, ArrayObject):
        # Chiama ricorsivamente per estrarre i dati da ogni elemento
        streams = [extract_content_stream_data(p) for p in content_object]
        return '\n'.join(streams)
    
    # CASO 4: Stream Object diretto (ha i dati)
    if hasattr(content_object, 'get_data'):
        return content_object.get_data().decode('latin-1')
        
    return ""

def optimize_lego_pdf_for_printing(input_filename, output_filename):
    """
    Sostituisce le occorrenze di colore blu (presunto sfondo) con il bianco 
    nel content stream di un PDF.
    """
    print(f"Inizio elaborazione PDF: {input_filename}")
    try:
        if not os.path.exists(input_filename):
            return f"Errore: File '{input_filename}' non trovato."
            
        reader = pypdf.PdfReader(input_filename)
        writer = pypdf.PdfWriter()
        
        # --- Pattern di Riconoscimento e Sostituzione Colore ---
        blue_fill_command_k = re.compile(r'([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) K', re.IGNORECASE)
        white_replacement_k = '0.0 0.0 0.0 0.0 K' 
        blue_fill_command_rg = re.compile(r'([\d\.]+) ([\d\.]+) ([\d\.]+) rg', re.IGNORECASE)
        white_replacement_rg = '1.0 1.0 1.0 rg'
        
        pages_processed = 0

        for i, page in enumerate(reader.pages):
            content_object = page.get("/Contents")
            content_stream = extract_content_stream_data(content_object)
            
            original_stream = content_stream 

            # Applicazione della sostituzione colore
            new_content_stream = blue_fill_command_k.sub(lambda m: white_replacement_k, content_stream)
            new_content_stream = blue_fill_command_rg.sub(lambda m: white_replacement_rg, new_content_stream)

            # Se lo stream è stato modificato, lo si riscrive nella pagina
            if new_content_stream != original_stream:
                
                # Creiamo un nuovo oggetto StreamObject diretto
                new_stream_obj = StreamObject()
                
                # Aggiungiamo i dati codificati
                new_stream_obj.set_data(new_content_stream.encode('latin-1'))
                
                # CORREZIONE CRITICA: Assegnazione usando NameObject come chiave
                # per risolvere il ValueError e superare l'ultimo blocco.
                page[NameObject("/Contents")] = new_stream_obj
                
                pages_processed += 1
            
            # Aggiunge la pagina al writer
            writer.add_page(page)

        # Scrive il PDF finale
        with open(output_filename, "wb") as output_file:
            writer.write(output_file)
            
        return f"✅ Elaborazione completata! Modificate {pages_processed} pagine. Nuovo file: '{output_filename}'"

    except Exception as e:
        error_info = f"{type(e).__name__}: {e}\n\nTraceback:\n{traceback.format_exc()}"
        return f"❌ Si è verificato un errore durante l'elaborazione: {error_info}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python lego_pdf.py <nome_file_input.pdf>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    
    base, ext = os.path.splitext(input_file_name)
    output_file_name = f"{base}_optimized{ext}"
    
    print(f"File di input: {input_file_name}")
    print(f"File di output: {output_file_name}")
    print("---")
    
    result = optimize_lego_pdf_for_printing(input_file_name, output_file_name)
    print(result)

if __name__ == "__main__":
    main()
