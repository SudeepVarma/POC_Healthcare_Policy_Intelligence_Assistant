"""
Description: The Application Presentation Layer or Streamlit UI Layer. Integrates parsing, Vector DB indexing, structured multi-stage parsing workflows, and rules sandbox environments into an interactive portal.
Author: Sudeep Varma K
Date: 2026-06-27
"""
import streamlit as st
import json
import parser
import rag
import llm
import validator
from schemas import PolicySummary

st.set_page_config(page_title="Enterprise Health Intelligence Engine", layout="wide")
st.title("Enterprise Healthcare Content Intelligence Portal (Basic PoC/pre-prototype)")
st.caption("Basic PoC grade architecture featuring local ingestion, vector stores, and execution validation sandboxes.")

# Create main operational processing tracks
tab1, tab2, tab3 = st.tabs(["Intelligent Ingestion & RAG", "Policy Shift Audit (Diff)", "Policy-To-Code Sandbox"])

#  TAB 1: RETRIEVAL AUGMENTED GENERATION TRACK
with tab1:
    st.header("1. Document Ingestion Pipeline")
    st.write("Extract text, index chunks, and query content using a verified local RAG pipeline.")

    uploaded_file = st.file_uploader("Upload Policy Document (PDF)", type="pdf")

    if uploaded_file:
        # Extract raw document text layers
        document_raw_text = parser.extract_pdf_text(uploaded_file)
        st.success("Document successfully parsed from memory buffer!")

        with st.expander("Preview Raw Text Extraction Layers (First 1,000 characters)"):
            st.text(document_raw_text[:1000])

        if st.button("Index and Vectorize Document"):
            with st.spinner("Processing text: chunking documents and building FAISS/Chroma vectors..."):
                rag.add_document(document_raw_text)
                st.success("Vector spaces successfully mapped inside local ChromaDB storage volumes!")

    st.markdown("---")
    st.header("2. Verified RAG Query Studio")
    user_query = st.text_input("Ask a question regarding your ingested healthcare policies:", placeholder="e.g., What are the prior authorization conditions for outpatient MRI scans?")

    if user_query:
        with st.spinner("Querying vector indices and executing model context evaluation..."):
            # Retrieve vector neighbors
            matched_contexts = rag.retrieve(user_query)

        with st.expander("View Inspected RAG Context Chunks"):
            st.info(matched_contexts)

        # Compose bounded verification prompts
        rag_prompt = f"Context:\n{matched_contexts}\n\nQuestion: {user_query}\n\nAnswer the question using ONLY the provided context blocks. Answer the following question in 2 to 3 cohesive paragraphs. Do not use bullet points, numbered lists, or dash-separated lists under any circumstances. If the answer is missing, state that it is not found."

        rag_response = llm.ask(rag_prompt, system_prompt="You are a strict healthcare analytics compliance checker.")
        st.markdown("System Inference Output")
        st.write(rag_response)

    st.markdown("---")
    st.header("3. Structured Compliance Extraction")
    st.write("Forces unstructured documents into schema-validated JSON outputs.")

    if st.button("Generate Validated Schema Extraction"):
        # Pull text contexts to extract keys against
        active_contexts = rag.retrieve("Identify contract title, coding metadata, prerequisites, and penalty matrices.")

        json_extraction_prompt = f"""Read the healthcare policy context below.
            Return ONLY valid JSON corresponding exactly to the requested structural format keys. Do not include markdown wraps like json.
    
            Template Structure:
            {{
                "title": "String representation of name",
                "effective_date": "Date format string",
                "billing_codes": ["List of target codes"],
                "prerequisites": ["List of protocol criteria requirements"],
                "penalties": ["List of non-compliance results"],
                "summary": "High level description summary"
            }}
    
            Policy Context:
            {active_contexts}"""

        with st.spinner("Enforcing structural token outputs..."):
            raw_json_string = llm.ask(json_extraction_prompt, force_json=True)
            try:
                # Load string properties back to object representations
                parsed_json_object = json.loads(raw_json_string)
                # Validate structures over schema maps
                validated_schema_model = PolicySummary(**parsed_json_object)

                st.markdown("Schema Verification Successful")
                st.json(validated_schema_model.model_dump())
            except Exception as schema_error:
                st.error(f"Schema Validation Failure: {str(schema_error)}")
                st.code(raw_json_string)

#  TAB 2: POLICY COMPARISON TRACK
with tab2:
    st.header("Payer-Provider Structural Change Analyzer")
    st.write("Performs multi-document relative text audits to isolate regulatory shift metrics automatically.")

    col1, col2 = st.columns(2)
    with col1:
        base_clause = st.text_area("Historical Contract Clause Base (e.g., 2025)", value="Claims must be submitted within 180 days from the date of service. Late claims face a 10% penalty markdown adjustment.", height=150)
    with col2:
        target_clause = st.text_area("Revised Contract Clause Variant (e.g., 2026)", value="Claims must be submitted within 90 days from the date of service. Late claims will be denied completely with absolute forfeiture of provider reimbursement.", height=150)

    if st.button("Execute Differential Contract Audit"):
        diff_prompt = f"""Compare the following contract text changes. Point out changes to operational windows, payment parameters, and financial liability exposure.

        BASE VERSION:
        {base_clause}

        REVISED VARIANT:
        {target_clause}"""

        with st.spinner("Analyzing delta changes..."):
            diff_results = llm.ask(diff_prompt, system_prompt="You are an expert contract attorney auditing relative risk deltas.")
            st.markdown("Risk Discrepancy Matrix")
            st.info(diff_results)

#  TAB 3: POLICY TO CODE INTEGRATION SANDBOX
with tab3:
    st.header("Policy-to-Code Transformation Engine")
    st.write("Leverages two-stage structural prompt processing to systematically construct deterministic rule models directly from prose descriptions.")

    default_narrative = """If a patient is 18 or older and the admitting diagnosis code is ICD-10 'I10' (Essential Hypertension) and  their systolic blood pressure reading is historically recorded above 140 mmHg,  approve coverage."""

    narrative_input = st.text_area("Input Natural Language Medical Rule/Policy:", value=default_narrative, height=130)

    # Track states persistently between code gen iterations
    if "synthesized_code" not in st.session_state:
        st.session_state.synthesized_code = ""

    if st.button("Compile Prose Into Executable Rules"):
        # Stage 1: Build Intermediate Representation JSON Map
        stage_1_prompt = f"""Convert this narrative policy into structural configuration parameters mapping conditionals, actions, and boundaries.
        Return JSON matching this template map:
        {{
            "condition": "textual condition map description",
            "action": "action taken code",
            "exception": "exception rules matching cases"
        }}

        Narrative Context:
        {narrative_input}"""

        with st.spinner("Stage 1: Extracting Intermediate Condition Maps (JSON)..."):
            intermediate_json = llm.ask(stage_1_prompt, system_prompt="You are a logic processing core.", force_json=True)
        # Stage 2: Translate Intermediate Representation into Pure Python Code Block
        stage_2_prompt = f"""Using this structured JSON specification, generate a Python function block named `check_coverage(age: int, diagnosis: str, bp: int) -> bool`. Return ONLY valid executable Python source statements. No comments, no markdown fences, no formatting wrappers. Returning illegal characters breaks processing pipelines.Ruleset JSON Specification:{intermediate_json}"""

        with st.spinner("Stage 2: Synthesizing Production Python Code Targets..."):
            pure_python_code = llm.ask(stage_2_prompt, system_prompt="You are a precise Python code compiler engine. You output pure functional definitions containing no prose wrappers.")
            # Sanitize raw code block enclosures if the model injected them despite explicit system rules
            clean_code = pure_python_code.replace("```python", "").replace("```", "").strip()
            st.session_state.synthesized_code = clean_code

    if st.session_state.synthesized_code:
        st.markdown("Synthesized Code Production Output")
        st.code(st.session_state.synthesized_code, language="python")

        st.markdown("---")
        st.header("Automated Rule Engine Sandbox Validation")
        st.write("Feed live application telemetry parameters directly into your newly generated logic code to test edge outcomes interactively.")
        # Build form components dynamically matching test arguments
        v_col1, v_col2, v_col3 = st.columns(3)
        with v_col1:
            test_age = st.number_input("Patient Evaluation Age", min_value=0, max_value=120, value=45)
        with v_col2:
            test_diag = st.text_input("ICD-10 Admitting Diagnosis Code", value="I10")
        with v_col3:
            test_bp = st.number_input("Recorded Systolic Blood Pressure", min_value=50, max_value=250, value=150)

        if st.button("Trigger Sandbox Verification Match"):
            test_arguments = {"age": test_age, "diagnosis": test_diag, "bp": test_bp}
            # Execute validation pipeline in the isolated sandbox engine
            sandbox_report = validator.execute_generated_rules(st.session_state.synthesized_code, test_arguments)
            if sandbox_report["success"]:
                st.markdown("Engine Assessment Outcome")
                if sandbox_report["output"] is True:
                    st.success(f" Approved: Rule engine returned validation code target evaluation match = TRUE")
                else:
                    st.error(f" Denied: Rule engine returned validation code target evaluation match = FALSE")
            else:
                st.error(f"Rule Execution Crash: {sandbox_report['error']}")